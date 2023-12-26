# PCS3616 - Laboratório 3 - GDB e MVN

## **Debugger: gdb**

O gdb é um **debugger**: um programa que permite acompanhar a execução
de um programa e também interferir nela. O gdb funciona com muitas
linguagens, mas as mais comuns são C e C++.

O uso do gdb será demonstrado a partir do exemplo abaixo, que mostra
como descobrir a causa de um erro de *segmentation fault* em um
programa. Esse exemplo é uma tradução/adaptação do original disponível
[aqui](http://www.unknownroad.com/rtfm/gdbtut/gdbsegfault.html).

### Usando o gdb para resolver um problema de *segfault*

Neste exemplo, você irá aprender a usar o gdb para descobrir por que o
programa abaixo, quando executado, causa um erro de *segmentation
fault*.

O programa deveria ler uma linha de texto do usuário e imprimi-la. No
entanto, veremos que, do jeito como está, o resultado não é exatamente
esse\...

**Versão inicial (com bug) do programa:**

  ```c
  #include <stdio.h>
  #include <stdlib.h>
  
  int main(int argc, char **argv) {
    printf("Digite um texto qualquer e pressione Enter ao final:n");
    
    char *buf;
    buf = malloc(1<<31);
    fgets(buf, 1024, stdin);
    
    printf("Texto digitado foi:n");
    printf("%s\n", buf);
    
    return 1;
  }
  ```

Crie um arquivo chamado segfault-example.c, com o conteúdo acima.
Compile o arquivo usando o gcc e o execute, para verificarmos se
realmente existe um problema:

```bash
gcc -o segfault-example segfault-example.c
./segfault-example
```

Você deve ter observado que, realmente, o programa termina com erro
antes de imprimir a linha digitada pelo usuário. Vamos usar o gdb,
então, para descobrir o motivo.

O primeiro passo é recompilar o arquivo usando a flag -g, que faz com
que o gcc compile o programa de uma forma ligeiramente diferente,
incluindo símbolos que serão usados pelo gdb.

```bash
gcc -g -o segfault-example segfault-example.c
```

Agora, execute o programa novamente, dessa vez pelo gdb:

```bash
$ gdb segfault-example
# [várias linhas na saída, omitidas]
Reading symbols from segfault-example...done.
(gdb)
```

Nesse ponto, o gdb está pronto e aguardando instruções. Para começar,
vamos simplesmente executar o programa usando o comando run e ver o que
acontece:

```bash
(gdb) run
Starting program:
/home/deborasetton/Documents/Mestrado/Monitoria/PCS3616-Systems-Programming/aula2/segfault-example
Digite um texto qualquer e pressione Enter ao final:
QUALQUER COISA AQUI

Program received signal SIGSEGV, Segmentation fault.
__GI__IO_getline_info (fp=fp@entry=0x7ffff7dd3980 <_IO_2_1_stdin_>, buf=buf@entry=0x0,
n=1022, delim=delim@entry=10, extract_delim=extract_delim@entry=1, eof=eof@entry=0x0) at
iogetline.c:86
86 iogetline.c: No such file or directory.
(gdb)
```

O gdb executa o programa até onde consegue e para novamente, informando
que recebeu o sinal SIGSEGV do sistema operacional. Isso significa que o
programa tentou acessar uma região de memória inválida.

Vamos usar o comando backtrace para descobrir onde exatamente o programa
travou:

```bash
(gdb) backtrace
#0 __GI__IO_getline_info (fp=fp@entry=0x7ffff7dd3980
<_IO_2_1_stdin_>, buf=buf@entry=0x0, n=1022, delim=delim@entry=10,
extract_delim=extract_delim@entry=1, eof=eof@entry=0x0) at
iogetline.c:86
#1 0x00007ffff7a7f188 in __GI__IO_getline
(fp=fp@entry=0x7ffff7dd3980 <_IO_2_1_stdin_>, buf=buf@entry=0x0,
n=<optimized out>, delim=delim@entry=10,
extract_delim=extract_delim@entry=1) at iogetline.c:38
#2 0x00007ffff7a7dfc4 in _IO_fgets (buf=0x0, n=<optimized out>,
fp=0x7ffff7dd3980 <_IO_2_1_stdin_>) at iofgets.c:56
#3 0x0000000000400647 in main (argc=1, argv=0x7fffffffd5c8) at
segfault-example.c:10
(gdb)
```

Repare que a saída do comando faz referência a alguns arquivos que o
programa usa, mas que não fomos nós que escrevemos, como iogetline.c e
iofgets.c.

Como estamos interessados no nosso próprio código, vamos usar o comando
frame para ir até o frame **3**, que é o frame que fala sobre o nosso
arquivo, segfault-example.c:

```bash
(gdb) frame 3
#3 0x0000000000400647 in main (argc=1, argv=0x7fffffffd5c8) at
segfault-example.c:10
10 fgets(buf, 1024, stdin);
(gdb)
```

Ok, então o programa travou na chamada à função fgets. De maneira geral,
sempre podemos assumir que funções da biblioteca padrão, como esta,
estão funcionando \-- se este não for o caso, o problema é muito maior.

Portanto, o problema deve estar em um dos 3 argumentos que passamos para
a função. Talvez você não saiba, mas stdin é uma variável global que é
criada pela biblioteca stdio, então este argumento podemos assumir que
está ok. Resta o argumento buf.

Vamos usar o comando print para inspecionar o valor desta variável:

```bash
(gdb) print buf
$1 = 0x0
(gdb)
```

O valor da variável é 0x0, que é o ponteiro nulo. Isso não é o que
queremos \-- buf deveria apontar para uma área de memória que foi
alocada na chamada ao malloc (veja o código).

Portanto, vamos ter que descobrir o que aconteceu aqui. Mas antes,
podemos encerrar a instância atual do programa (que já nos deu
informações suficientes e não tem mais o que executar) usando o comando
kill:

```bash
(gdb) kill
Kill the program being debugged? (y or n) y
(gdb)
```

Após este comando, estamos novamente no início do gdb. Desta vez, vamos
colocar um breakpoint na linha do código que chama o malloc:

```bash
(gdb) break segfault-example.c:9
Breakpoint 1 at 0x40062f: file segfault-example.c, line 9.
(gdb)
```

Agora, vamos rodar o programa novamente:

```bash
(gdb) run
Starting program:
/home/deborasetton/Documents/Mestrado/Monitoria/PCS3616-Systems-Programming/aula2/segfault-example
Digite um texto qualquer e pressione Enter ao final:

Breakpoint 1, main (argc=1, argv=0x7fffffffd5c8) at segfault-example.c:9
9 buf = malloc(1<<31);
(gdb)
```

Primeiro, vamos ver qual é o valor de buf antes da chamada ao malloc,
usando o comando print. Uma vez que essa variável ainda não foi
inicializada, esperamos que o valor seja inválido, e realmente é:

```bash
(gdb) print buf
$1 = 0x0
(gdb)
```

Agora, vamos usar o comando next para executar apenas esta linha de
código e parar novamente, para podermos ver o que aconteceu com a
variável:

```bash
(gdb) next
10 fgets(buf, 1024, stdin);
(gdb) print buf
$2 = 0x0
(gdb)
```

Após a chamada, verificamos que buf continua inválido, apontando para
NULL. Por quê? Se você consultar a documentação do malloc, descobrirá
que essa função retorna NULL quando não consegue alocar a quantidade de
memória solicitada. Portanto, a chamada ao malloc feita pelo nosso
programa deve ter falhado. Vamos olhar esssa chamada novamente:

```
buf = malloc(1<<31);
```

Bom\... O valor da expressão 1 \<\< 31 (o inteiro 1 deslocado 31 bits à
esquerda) é 429497295 ou 4GB. Poucos sistemas operacionais alocariam
esta quantidade de memória para um único programa, a não ser com
configurações especiais, então é claro que o malloc falhou. Além disso,
nós só estamos lendo 1024 bytes com o fgets, então para que alocar tanta
memória?

Mude o valor 1\<\<31 no código-fonte para 1024, compile e execute o
programa novamente:

```bash
$ gcc -o segfault-example segfault-example.c
$ ./segfault-example
Digite um texto qualquer e pressione Enter ao final:
QUALQUER COISA AQUI
Texto digitado foi:
QUALQUER COISA AQUI
```

Problema resolvido! \\o/

E agora você sabe como depurar segfaults usando o gdb, o que é
extremamente útil. Finalmente, este exemplo também ilustra um outro
ponto muito importante: **sempre verifique o valor retornado pelo
malloc!**

# Baixar a MVN

A MVN está em um [submodulo](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

Você pode baixar junto automaticamente ao clonar
```bash
$ git clone --recurse-submodules <URI>
```

Ou caso já tenha clonado o repositorio você pode inicializar o submodulo.
```bash
$ git submodule update --init
```
Para rodar o simulador da MVN, a partir da raiz do repositório, você pode iniciar um terminal Python e 
importar o monitor
```python
$ python3
>>> from MVN import mvnMonitor
```
ou você pode executar diretamente com
```bash
$ python3 -m MVN.mvnMonitor
```

O monitor da MVN será iniciado, esse monitor fará a integração entre
seus códigos e o simulador. Na tela aparecerão as opções de comando que
você pode usar (sugestão: gaste algum tempo analisando as funções).

# **Exercícios**

| Atenção: em todos os exercícios, escrever os comentários apropriados para **todas** as instruções do programa.
-----------------------------------------------------------------------|

## 1) **ex1-soma.mvn**
Escrever um programa que soma o valor das posições de memória 0x010 e 
0x012 e armazena o resultado na posição 0x014. As parcelas da soma devem 
ser -111 e 333 (usar representação em complemento de 2).

## 2) **ex2-divisao.mvn**
Escrever um programa que executa a seguinte operação Z = (X-Y)/W, na qual as variáveis X, Y e W
são valores dados armazenados nas posições 0x010, 0x012 e 0x014, respectivamente. O resultado (Z)
deve ser armazenado na posição 0x016. Além disso, lembre-se que a MVN não trata exceções, ou seja,
caso W seja zero o programa da MVN irá terminar antecipadamente, pois ocorrerá uma divisão por zero.
Dessa forma, o seu código deve tratar esse caso, impedindo que a divisão ocorra e armazenando o valor
1 em Z.

# Dica:

Informação importante sobre a matéria da disciplina:

<img src="./media/image1.jpg" width=50%>
