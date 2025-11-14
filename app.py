"""
#  **Interface - reasoning model**

**Developer:** Adonias Caetano de Oliveira

**Version:** Interface with reasoning model

"""## **Importing library**"""

# Auxiliaries
import pandas as pd
import random
import time
import datetime
import numpy as np
import io
import re
import os
from datetime import datetime

# Interface with Gradio
import gradio as gr

"""## **Reading the data set**"""

# read the data
dataset = pd.read_excel("base.xlsx")

current_examples = dataset["text"].values.tolist()

"""## **Interface XAI**"""

STATUS_STARTING_PARTICIPATION = 0
STATUS_ANSWERING_SENTENCE = 1
STATUS_EVALUATING_RESPONSE = 2
STATUS_END_PARTICIPATION = 3

MODE_WITH_REASONING = 0
MODE_WITHOUT_REASONING = 1
modelos = ["model with reasoning", "model without reasoning"]

MAX_QUANT_TESTES = 10 # a quantidade máxima de testes que o usuário consegue realizar na interface
TESTE_ATUAL = 0
testes = {} # Armazena os testes realizados pelo usuário
testes["sentence"] = []
testes["response"] = []
testes["mode"] = []
testes["understanding"] = []
testes["relevant"] = []
testes["correct"] = []
testes["trust"] = []

# Inicializando todas as variáveis
contagem = {}
contagem[MODE_WITH_REASONING] = 0
contagem[MODE_WITHOUT_REASONING] = 0
mode = -1
status = STATUS_STARTING_PARTICIPATION
inicio = 0

def status_controlling_experiment():
  global mode
  global contagem
  global status
  global inicio
  global TESTE_ATUAL
  global MAX_QUANT_TESTES

  # seleciona o modo de resposta se o participante está iniciando o experimento
  if status == STATUS_STARTING_PARTICIPATION:
    inicio = time.time()  # Marca o tempo inicial
    mode = random.randint(0, 1)
    contagem[mode] += 1
    status = STATUS_ANSWERING_SENTENCE
    TESTE_ATUAL = 0
  # seleciona o modo de resposta se o participante já fez um experimento ou mais
  elif status == STATUS_ANSWERING_SENTENCE:

    mode = random.randint(0, 1)

    if contagem[mode] < MAX_QUANT_TESTES/2: # Seleciona um modo de resposta
      contagem[mode] += 1
      TESTE_ATUAL += 1
    else:
      mode = 1 - mode
      if contagem[mode] < MAX_QUANT_TESTES/2: # Seleciona outro modo de resposta
        contagem[mode] += 1
        TESTE_ATUAL += 1
      else: # Se todos os modos de respostas já foram testados, então deve finalizar o experimento
        mode = -1
        status = STATUS_END_PARTICIPATION

  if status == STATUS_ANSWERING_SENTENCE:
    testes["mode"].append(modelos[mode])

    if TESTE_ATUAL > 0:
        gr.Warning(f"Falta(m) testar mais {MAX_QUANT_TESTES - TESTE_ATUAL} sentenças de {MAX_QUANT_TESTES}")
  else:
    status_experiment_finalize()

def get_labels(sentences):
  labels = []
  for sentence in sentences:
    filtro = dataset["text"] == sentence
    df_filtrado = dataset.loc[filtro, ["label"]]
    labels.append(df_filtrado["label"].values[0])
  return labels

def status_experiment_finalize():
  global inicio
  fim = time.time()  # Marca o tempo final
  tempo = fim - inicio  # Calcula o tempo decorrido

  quant_sentencas = len(testes["sentence"])
  agora = datetime.now()
  data_formatada = agora.strftime("%d-%m-%Y %H:%M:%S")
  labels = get_labels(testes["sentence"])
  quant_classes = len(labels)

  print(f"Quantidade de sentenças testadas: {quant_sentencas}")
  print(f"Quantidade de classes testadas: {quant_classes}")
  print(f"Tempo de experimento: {tempo:.6f} segundos")

  registro_experimento = {
    "Sentenças testadas" : testes["sentence"],
    "Classes testadas" : labels,
    "Modelos testados" : testes["mode"],
    "Dia do experimento" : [data_formatada]*quant_sentencas,
    "Tempo de experimento" : [tempo]*quant_sentencas,
    "Compreensão": testes["understanding"],
    "Corretude": testes["relevant"],
    "Relevância":  testes["correct"],
    "Confiança":  testes["trust"]
  }

  df = pd.DataFrame(registro_experimento)

  data_formatada_segura = data_formatada.replace(":", "-")
  nome_arquivo_output = f'{data_formatada_segura}.xlsx'
  
  caminho_base = os.path.dirname(os.path.abspath(__file__))
  caminho_output = os.path.join(caminho_base, nome_arquivo_output)

  print(caminho_base)
  print(caminho_output)

  try:
    df.to_excel(caminho_output, index=False)
    print(f"DataFrame salvo como '{nome_arquivo_output}' em: {caminho_output}")
    gr.Warning(f"Você finalizou a participação neste estudo!\nVocê levou {tempo:.6f} segundos\n.")
  except Exception as e:
    print(f"Erro ao salvar os resultdos: {e}")
    gr.Warning(f"Erro ao salvar o DataFrame como Excel\n.")

def get_answer(sentence):
  global mode
  filtro = dataset["text"] == sentence

  if mode == MODE_WITH_REASONING:
    df_filtrado = dataset.loc[filtro, ["reasoning"]]
    answer =  df_filtrado["reasoning"].values[0]
    answer = re.sub(r"<pensar>", "**Pensando passo a passo**\n", answer)
    answer = re.sub(r"</pensar>", "\n**fim do raciocínio**\n\n", answer)
  else:
    df_filtrado = dataset.loc[filtro, ["answer"]]
    answer = df_filtrado["answer"].values[0]

  return answer

def status_answering_sentence(sentence):
  global testes
  global TESTE_ATUAL
  global status

  if status == STATUS_END_PARTICIPATION:
    gr.Warning("Você já finalizou o experimento!")
    resposta = ""
  elif status == STATUS_EVALUATING_RESPONSE:
    gr.Warning("Você precisa avaliar a explicação atual e depois acionar o botão salvar avaliação!")
    last_sentence = testes["sentence"][-1]
    resposta = get_answer(last_sentence)
  elif status == STATUS_ANSWERING_SENTENCE:

    if sentence == "":
      gr.Warning("Você precisa selecionar uma sentença para testar!")
      resposta = ""
    elif sentence in testes["sentence"]:
      gr.Warning("Esta sentença já foi testada! Por favor, escolha outra.")
      resposta = ""
    else:
      # seleciona a explicação adequada
      testes["sentence"].append(sentence)
      resposta = get_answer(sentence)
      testes["response"].append(resposta)
      status = STATUS_EVALUATING_RESPONSE

  return resposta

def status_evaluating_response(understanding, relevant, correct, trust):
  global status

  if status == STATUS_END_PARTICIPATION:
    gr.Warning("Você já finalizou o experimento!")
  elif status == STATUS_ANSWERING_SENTENCE:
    gr.Warning("Você precisa selecionar uma sentença e depois acionar o botão para explicar se a sentença contém ou não ideação suicida!")
  elif status == STATUS_EVALUATING_RESPONSE:
    if not understanding or not relevant or not correct or not trust:
      gr.Warning("Você precisa preencher todas as avaliações!")
      return testes["sentence"][-1], testes["response"][-1], understanding, relevant, correct, trust
    else:
      testes["understanding"].append(understanding)
      testes["relevant"].append(relevant)
      testes["correct"].append(correct)
      testes["trust"].append(trust)
      gr.Warning("Avaliação registrada com sucesso!")
      status = STATUS_ANSWERING_SENTENCE

      if testes["sentence"][-1] in current_examples:
          current_examples.remove(testes["sentence"][-1])

      status_controlling_experiment()

  return "", "", None, None, None, None

custom_css = """
.radio-group label {
    font-weight: bold !important;
}
.meu-botao-verde {
      background-color: green !important;
      color: white !important;
      border-color:  green !important;
}

.meu-botao-vintage {
      background-color: vintage !important;
      color: black !important;
      border-color: vintage !important;
}
"""

status_controlling_experiment()

with gr.Blocks() as demo_llm:

  gr.HTML(f"<style>{custom_css}</style>")

  with gr.Row():
    gr.Markdown(
      f"""
      # Interface de explicação se a sentença contém ideação suicida.
      ## <span style='color: blue;'>Saudações, participante!</span>
      ### <span style='color: red;'> Neste experimento você vai testar {MAX_QUANT_TESTES} sentenças </span>
      ### <span style='color: green;'> Selecione um exemplo de sentenca abaixo do Twitter</span>
      """
    )

  with gr.Row():
    with gr.Column(scale=1, min_width=300):
      input = gr.TextArea(label="Entrada:", placeholder="Selecione uma sentença abaixo para explicar se contém ideação suicida.", interactive=False)

      exemplos_componente = gr.Examples(
            examples = current_examples,
            inputs = input,
            label = "Exemplos de sentenças."
      )
    with gr.Column(scale=2, min_width=300):
      #Classificação
      classificar_btn = gr.Button("Me explique por que esta sentença possui ou não ideação suicida")

      text_resposta = gr.Markdown(label="Resposta:")

      classificar_btn.click(fn=status_answering_sentence, inputs=input, outputs=[text_resposta] )

      gr.Markdown(
      f"""
      #### <span style='color: blue;'>Marque o item abaixo que melhor reflete sua opinião sabendo que 0 é a pontuação mínima e 5 a pontuação máxima.</span>
      """
      )

      radio_entendimento = gr.Radio(
        ["(1) Discordo totalmente", "(2) Discordo parcialmente", "(3) Neutro", "(4) Concordo parcialmente", "(5) Concordo totalmente"],
        label = "EU  COMPREENDI esta explicação dentro do contexto da identificação de ideação suicida.",
        elem_classes=["radio-group"]
      )
      #radio_entendimento.change(fn=avaliar, inputs=radio_entendimento)

      radio_relevancia = gr.Radio(
         ["(1) Discordo totalmente", "(2) Discordo parcialmente", "(3) Neutro", "(4) Concordo parcialmente", "(5) Concordo totalmente"],
        label = "EU CONSIDERO RELEVANTE esta explicação para identificar ideação suicida, pois ela apresenta coerência e consistência ao abordar exclusivamente esse tema sensível.",
        elem_classes=["radio-group"]
      )
      #radio_relevancia.change(fn=avaliar, inputs=radio_relevancia)

      radio_correta = gr.Radio(
         ["(1) Discordo totalmente", "(2) Discordo parcialmente", "(3) Neutro", "(4) Concordo parcialmente", "(5) Concordo totalmente"],
        label = "EU CONSIDERO CORRETA esta explicação para identificar ideação suicida em texto, devido à precisão e veracidade das informações apresentadas.",
        elem_classes=["radio-group"]
      )
      #radio_correta.change(fn=avaliar, inputs=radio_correta)

      radio_confianca = gr.Radio(
         ["(1) Discordo totalmente", "(2) Discordo parcialmente", "(3) Neutro", "(4) Concordo parcialmente", "(5) Concordo totalmente"],
        label = "EU CONFIO nesta explicação gerada pela Inteligência Artificial para identificar ideação suicida em texto",
        elem_classes=["radio-group"]
      )
      #radio_confianca.change(fn=avaliar, inputs=radio_confianca)

      salvar_btn = gr.Button("Salvar minha avaliação", elem_classes=["meu-botao-vintage"])
      salvar_btn.click( fn=status_evaluating_response, inputs=[radio_entendimento, radio_relevancia, radio_correta, radio_confianca], outputs=[input, text_resposta, radio_entendimento, radio_relevancia, radio_correta, radio_confianca] )



#demo_llm.launch(debug=True, share=True, inline=False)
demo_llm.launch(share=True)
#demo_llm.queue().launch(share=True)
#demo_xai_digitacao.launch(inline=False)
