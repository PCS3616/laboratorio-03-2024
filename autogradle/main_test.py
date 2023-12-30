from pathlib import Path
import subprocess
import re
import tempfile

submission_path = Path("./submission")

def limpa(string):
    res=string.split(" ")
    res=list(filter(None, res))
    return int(res[1]+res[2],16)

def run_mvn(input_text):
    # I hate the current MVN
    # A good class solve this, but now are a really mess code

    p = subprocess.run(
        [
            "python", 
            "-m", 
            "MVN.mvnMonitor"
        ],
        input=input_text,
        capture_output=True, 
        text=True,
    )
    return p.stdout

def test_1():
    filecode = submission_path / "ex1-soma.mvn"
    assert filecode.exists(), f"A submissão não contém o arquivo '{filecode.name}'"

    inputs = [
        f"p {filecode.as_posix()}",
        "r",
        "",
        "n",
        "",
        "m 0010 0015",
        "x"
    ]

    output = run_mvn('\n'.join(inputs))

    mem_output = output.split('\n')[-4]

    assert \
        mem_output=="0010:  01  4d  ff  91  00  de  " \
        or mem_output=="0010:  ff  91  01  4d  00  de  ", \
       f"Seu código não está correto"

def test_2(x: int = 0, y: int = 0, w: int = 0):
    filecode = submission_path / "ex2-divisao.mvn"
    assert filecode.exists(), f"A submissão não contém o arquivo '{filecode.name}'"

    x_str = "{:04X}".format(x)
    y_str = "{:04X}".format(y)
    w_str = "{:04X}".format(w)
    input_file = tempfile.NamedTemporaryFile(mode='w')
    input_file.writelines([
        f"0010	{x_str}\n",
        f"0012	{y_str}\n",
        f"0014	{w_str}\n"
    ])
    input_file.flush()

    output_file = tempfile.NamedTemporaryFile(mode='r')

    inputs = [
        f"p {filecode.as_posix()}",
        "",
        f"p {input_file.name}",
        "",
        "r",
        "0",
        "n",
        "",
        f"m 0016 0017 {output_file.name}",
        "",
        "x",
        "",
    ]

    run_mvn('\n'.join(inputs))

    z = limpa(output_file.read())

    if w == 0:
      assert z == 1, \
        f"Seu código não está correto\nConfira seu envio."
    else:
      assert z == int((x-y)/w), \
        f"Seu código não está correto\nConfira seu envio."

def test_2_1():
  test_2(8, 2, 2)

def test_2_2():
  test_2(49, 6, 42)

def test_2_3():
  test_2(128, 64, 0)
