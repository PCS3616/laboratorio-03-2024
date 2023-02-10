from pathlib import Path
import subprocess
import re
import tempfile

submission_path = Path("./submission")

def twos_complement(hexstr,bits):
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

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

def test_2():
    filecode = submission_path / "ex2-subtracao.mvn"
    assert filecode.exists(), f"A submissão não contém o arquivo '{filecode.name}'"
    
    with open(filecode, mode='r') as f:
        code = f.read().upper()

        assert len(re.findall(r"A[\dA-F]{3}", code)) > 0, \
            "O seu código deve conter uma chamada de subrotina"

        assert len(re.findall(r"B[\dA-F]{3}", code)) > 0, \
            "O seu código deve conter uma subrotina"

    inputs = [
        f"p {filecode.as_posix()}",
         "r",
         "",
         "n",
         "",
         "m 0010 0015",
         "x",
         "",
    ]

    output = run_mvn('\n'.join(inputs))

    saida=output.split("\n")[-6:-3]
    print(saida)

    nums=saida[-1].split("  ")
    x=twos_complement(nums[1]+nums[2], 16)
    y=twos_complement(nums[3]+nums[4], 16)
    r=twos_complement(nums[5]+nums[6], 16)

    assert x-y == r, \
        f"Seu código não está correto\nConfira seu envio."

def test_3():
    filecode = submission_path / "ex3-io.mvn"
    assert filecode.exists(), f"A submissão não contém o arquivo '{filecode.name}'"

    newcodefile = tempfile.NamedTemporaryFile(mode='w')

    with open(filecode) as f:
        new=re.sub("(e|E)100", "e300", f.read())
        newcodefile.write(new)
        newcodefile.flush()

    outputfile = tempfile.NamedTemporaryFile(mode='r')

    inputs = [
        f"p {newcodefile.name}",
        "s",
        "a",
        "3",
        "00",
        outputfile.name,
        "e",
        "r",
        "",
        "n",
        "07  54",
        "x",
    ]

    run_mvn('\n'.join(inputs))
    
    mvn_output = outputfile.read().replace('\n', '')
    assert mvn_output == "61", \
        f"Seu código não está correto\nConfira seu envio."
