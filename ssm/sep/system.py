# %%
import platform
import subprocess

# %%


def to_clipboard(text: str) -> None:
    opsys = platform.system().lower()
    if opsys in {"darwin", "linux"}:
        subprocess.run("pbcopy", text=True, input=text)
    elif opsys == "windows":
        subprocess.run(["echo", text, "|", "clip"], shell=True, check=True)
    else:
        raise Exception("unrecognized operating system")


# %%
