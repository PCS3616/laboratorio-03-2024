# PCS3616 - Laboratório 4 - MVN 1

Executar os comandos abaixo em um terminal.

**Instalação da MVN (simulador da Máquina de Von Neumann)**

```bash
cd \~/Documents/pcs3616
wget https://github.com/PCS-Poli-USP/MVN/archive/master.zip
unzip master.zip
rm master.zip

mv MVN-master/* .

rmdir MVN-master
```

Você pode notar que foram criados dois diretórios abaixo de pcs3616 que
você criou aula passada, são eles MVN e MLR. Pelas aulas próximas vamos
utilizar apenas o MVN, logo execute:

```bash
cd MVN
```

Para rodar o simulador da MVN:

```python
# Em um terminal Python
import mvnMonitor
```

O monitor da MVN será iniciado, esse monitor fará a integração entre
seus códigos e o simulador. Na tela aparecerão as opções de comando que
você pode usar (sugestão: gaste algum tempo analisando as funções).

# **Exercícios**

| Atenção: em todos os exercícios, escrever os comentários apropriados para **todas** as instruções do programa.
|-----------------------------------------------------------------------|

## 1) **ex1-soma.mvn**
Escrever um programa que soma o valor das posições de memória 0x010 e 
0x012 e armazena o resultado na posição 0x014. As parcelas da soma devem 
ser -111 e 333 (usar representação em complemento de 2).

## 2) **ex2-subtracao.mvn**
Escrever um programa que executa a subtração
de dois inteiros *em uma sub-rotina*. O programa principal
armazena os inteiros nas posições 0x010 (variável x) e 0x012 (variável
y) e chama a sub-rotina, que deve executar a operação x-y e armazenar o
resultado na posição de memória 0x014.

## 3) **ex3-io.mvn**
Escrever um programa que lê dois números do teclado
(`x` e `y`), e imprime o valor de `x+y`. Observações:

- `0 <= x`, `y <= 99`

- Os números devem ser lidos do teclado, em uma única linha, no
formato `<x-d1><x-d2><s><s><y-d1><y-d2>`, onde:

  - `<x-d1>` é o primeiro dígito de x. Se `x < 10`, o dígito
  informado deve ser `0`.

  - `<x-d2>` é o segundo dígito de `x`.

  - `<s>` é um espaço em branco

  - `<y-d1>` é o primeiro dígito de `y`. Se `y < 10`, o dígito
  informado deve ser `0`.

  - `<x-d2>` é o segundo dígito de `y`.

Por exemplo, \"07 54\" é uma entrada válida, e o programa deve imprimir
\"61\" na saída.

Dicas:

-   Use sub-rotinas para a conversão dos dígitos lidos em valores numéricos.

-   Veja o código de exemplo no [colinha da MVN](https://github.com/PCS3616/task-extra/blob/main/mvn_helper.md)

-   Consulte a [tabela ASCII](http://ascii.cl/)

Informação importante sobre a matéria da disciplina:

![did you know... in order to play the role of an insane and mentally depressed person the moviwe "Joker", Joaquin Phoenix started learning programming in assembly](./media/image1.jpg)
