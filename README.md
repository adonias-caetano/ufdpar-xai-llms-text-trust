
 # LLMs in Suicide Ideation Detection: Evaluation of Classifier Models and Analysis of the Impact of the Explainer Model on Trust

<p align="center">
This repository provides codes of LLMs evaluated, supplementary material, and questionnaires regarding the Level of Trust and quality of textual explanations provided by LLMs 

</p>


## 🔍 About This Project

This work extends the original Boamente architecture, integrating generative LLMs for suicidal ideation detection and evaluating the impact of textual explanations on trust. The proposed **Boamente Prisma** architecture classifies PT-BR texts and generates readable justifications for decisions using a second reasoning model. Both the prediction and explanation are delivered through a web interface designed for mental health professionals (MHPs).

## 🧪 Study Overview

The study was conducted remotely in a synchronous format with mental health professionals (MHPs), allowing wider geographic reach and participant diversity. The research followed three stages:

1. Informed consent + sociodemographic questionnaire
2. Experiment with textual explanations
3. Evaluation using the Perceived Quality of Explanation Questionnaire

Three explanation formats were compared:

* **CoT (Chain-of-Thought)** – explanations structured with step-by-step reasoning
* **Non-CoT** – brief explanations without explicit reasoning steps

The aim was to analyse how explanation style influences trust in Boamente Prisma.


## 📚  Dataset

The <a href="https://zenodo.org/records/10070747"><strong>original dataset</strong></a> used in this work contains **3,777 PT-BR sentences**, annotated by three psychologists and labeled into two classes representing the presence or absence of suicidal ideation.

* **Negative (no suicidal ideation): 2,687**  
* **Positive (suicidal ideation): 1,090**

The dataset is provided in CSV format with two columns: **text** (the sentence) and **target** (0 = negative, 1 = positive).

Preprocessing included the removal of hashtags, links, and special characters.  
No class balancing techniques were applied, preserving the natural distribution of the data.

## 🧠 Fine-tuning Setup

Models were fine-tuned for suicidal ideation classification using **stratified 5-fold cross-validation**, ensuring proportional class distribution across all folds.

Training was performed on a machine with **Intel i9 (13th Gen), 128GB RAM, NVIDIA RTX 4090**, using the **Unsloth (2025.10.10)** implementation with the default **QLoRA** configuration.


### ⚙ Training Framework

Fine-tuning was implemented using **Unsloth** with **QLoRA**, enabling efficient training through 4-bit quantisation + low-rank adaptation. Only LoRA matrices were updated, reducing GPU memory usage while maintaining performance. Parameter-Efficient Fine-Tuning (PEFT) was applied to optimise training.

## 🖥️ Development methodology

In this project, two prototypes of Boamente were developed using <a href="https://www.gradio.app/"><strong>Gradio</strong></a>. The first interface was implemented without using XAI methods, i.e., it only allows the typing of sentences and the activation of the "classify" function. The second interface allows the explanation of predictions using the Local Interpretable Model-Agnostic Explanations (<a href=" https://github.com/marcotcr/lime"><strong>LIME</strong></a>) method, in addition to also classifying sentences as "contains suicidal ideation" and "does not contain suicidal ideation".

## 🤖 Article in Review

Paper submitted to <a href="https://www.sciencedirect.com/journal/artificial-intelligence-in-medicine/publish/open-access-options"> <strong>Artificial Intelligence in Medicine</strong></a>

### [Paper Link]() 

## 👏 Contributing
 
If there is a bug, or other improvement you would like to report or request, we encourage you to contribute.

Please, feel free to contact us for any questions: 

* [![Gmail Badge](https://img.shields.io/badge/-ariel.teles@ifma.edu.br-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:ariel.teles@ifma.edu.br)](mailto:ariel.teles@ifma.edu.br )
* [![Gmail Badge](https://img.shields.io/badge/-adonias.oliveira@ifce.edu.br-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:adonias.oliveira@ifce.edu.br)](mailto:adonias.oliveira@ifce.edu.br )

## 📄 License

### <a href="https://doi.org/10.5281/zenodo.10070747"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.10070747.svg" alt="DOI"></a> 

## 📚 References

* <a href="https://www.mdpi.com/2227-9032/10/4/698"><strong>Paper about Boamente System</strong></a>.
* <a href="https://www.sciencedirect.com/science/article/pii/S1877050922009668"><strong>Paper about XAI Boamente System</strong></a>.
* <a href="https://www.scielo.br/j/csp/a/XrbVfvybPj9tvJ8qWv7j8VC/?lang=en"><strong>Paper about Generative LLMs (ChatGPT 3.5, Google Bard, and Microsoft Bing) vs BERT Models (BERTimbau and Multilingual)</strong></a>.

