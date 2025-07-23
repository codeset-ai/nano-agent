
import os
import time

import dotenv

from codeset import Codeset

from nano.tools import ToolStats
from nano.utils import warning

dotenv.load_dotenv()

CODESET_API_KEY = os.getenv("CODESET_API_KEY")


class CodesetAgent:
    def __init__(
        self,
        stats: ToolStats,
        sample_id: str,
        verbose: bool = False,
    ):
        self.stats = stats
        self.dataset = "gitbug-java" # TODO: make this configurable
        self.sample_id = sample_id
        self.verbose = verbose
        self.client = Codeset(
            api_key=CODESET_API_KEY,
        )
        self.session = self.client.sessions.create(
            dataset=self.dataset,
            sample_id=self.sample_id,
        )

    def shell(self, args: dict) -> str:
        command = args.get("cmd")
        if not command:
            return warning("shell: missing cmd")

        if self.verbose:
            print(f"running command: {command}")

        try:
            response = self.client.sessions.execute_command(
                session_id=self.session.session_id, command=command
            )
            self.stats.record_shell(cmd=command, success=True)
            if self.verbose:
                print(f"shell command completed: {response}")
            return f"stdout:\n{response.stdout}\nstderr:\n{response.stderr}"
        except Exception as e:
            self.stats.record_shell(cmd=command, success=False)
            return warning(f"shell command failed: {e}")

    def apply_patch(self, args: dict) -> str:
        file_path, search, replace = args.get("file_path"), args.get("search"), args.get("replace")
        if not file_path or not search or not replace:
            return warning("apply_patch: missing file_path, search, or replace")

        if self.verbose:
            print(f"applying patch:\n{file_path}, {search}, {replace}")

        try:
            self.client.sessions.str_replace(
                session_id=self.session.session_id,
                file_path=file_path,
                str_to_replace=search,
                str_to_insert=replace,
            )
            self.stats.record_patch(success=True)
            return "Patch applied successfully"
        except Exception as e:
            self.stats.record_patch(success=False)
            return warning(f"apply_patch failed: {e}")

    def verify(self) -> bool:
        if self.verbose:
            print("Verifying session...")

        # Start verification
        response = self.client.sessions.verify.start(session_id=self.session.session_id)

        # Wait for verification to complete
        while True:
            response = self.client.sessions.verify.status(
                job_id=response.job_id,
                session_id=self.session.session_id
            )
            if response.status in ["completed", "error", "cancelled"]:
                break
            time.sleep(1)

        if self.verbose:
            print(f"Verification completed: {response}")

        # Check if verification was successful
        if response.status == "completed" and response.result:
            return response.result.is_success
        else:
            return False

    def close(self):
        response = self.client.sessions.close(session_id=self.session.session_id)
        if self.verbose:
            cost = response.duration_seconds / 60 * 0.05
            print(f"Session duration: {response.duration_seconds:.2f}s")
            print(f"Approx. cost: ${cost:.4f}")
