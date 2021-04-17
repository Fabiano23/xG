# -*- coding: utf-8 -*-
"""Funções que serão utilizadas ao longo dos notebooks do projeto
"""

"""Bibliotecas"""

#Manipulação dos dados
import numpy as np
import pandas as pd

#Visualização
import seaborn as sns
import matplotlib.pyplot as plt
import FCPython

#Métricas de performance do modelo
from sklearn.metrics import precision_score, confusion_matrix

#Tamanho padrão das fontes nas figuras feitas com o seaborn neste arquivo
sns.set(font_scale=1.5)

#Tamanho padrão das figuras neste arquivo
plt.rcParams["figure.figsize"] = [14, 8]

#Dataset
chutes_modelo= pd.read_csv('todos_os_chutes_modelo.csv')


"""Plot de probabilidade por ângulo e/ou distância do chute em relação ao gol"""

def plot_prob(tipo= '', chutes_modelo= chutes_modelo, b= None, save= False):
    '''Plot da probabilidade de marcar de acordo com o ângulo do chute utilizando todos os dados'''
    
    #Histograma de duas dimensões: eixo x e y do chute sem considerar os pênaltis
    H_Chute=np.histogram2d(chutes_modelo[~chutes_modelo['subEventoNome'].isin(['Penalty'])]['X'], 
                       chutes_modelo[~chutes_modelo['subEventoNome'].isin(['Penalty'])]['Y'], 
                       bins=50, range=[[0, 100],[0, 100]])

    gols=chutes_modelo[~chutes_modelo['subEventoNome'].isin(['Penalty']) & chutes_modelo['Gol']==1]

    H_Gol=np.histogram2d(gols['X'], gols['Y'], bins=50, range=[[0, 100],[0, 100]])
    
    
    #Probabilidade de marcar de acordo com o ângulo e a distância do chute em relação ao gol
    #Total de chutes por ângulo
    total_chutes_por_angulo=np.histogram(chutes_modelo['Angulo']*180/np.pi,bins=40, range=[0, 150])

    #Total de gols por ângulo
    total_gols_por_angulo=np.histogram(gols['Angulo']*180/np.pi,bins=40,range=[0, 150])

    #Probabilidade de marcar o gol de acordo com o ângulo do chute 
    #-> (gols marcados | angulo) / (chutes feitos | angulo)
    prob_gol_angulo=np.divide(total_gols_por_angulo[0], total_chutes_por_angulo[0])

    #Calculo de angulo medio
    angulo= total_chutes_por_angulo[1]
    angulo_medio= (angulo[:-1] + angulo[1:])/2

    #Total de chutes por distância
    total_chutes_por_dist=np.histogram(chutes_modelo['distanciaGol'],bins=40,range=[0, 70])

    #Total de gols por distância
    total_gols_por_dist=np.histogram(gols['distanciaGol'],bins=40,range=[0, 70])

    #Probabilidade de gol por distância
    prob_gol_dist=np.divide(total_gols_por_dist[0], total_chutes_por_dist[0])

    #Calculo de distancia media
    distancia=total_chutes_por_dist[1]
    dist_media= (distancia[:-1] + distancia[1:])/2
    
    #Valores de ângulos inventados
    x=np.arange(150, step=0.1)
    
    #Modelo likelihood utilizando amostra dos dados
    if tipo == 'likelihood':
        b=[3, -3] #parâmetros
        y=1/(1+np.exp(b[0]+b[1]*x*np.pi/180)) #Calculo de y dado x e os coeficientes
        xG=1/(1+np.exp(b[0]+b[1]*chutes_modelo['Angulo'])) 
        chutes_modelo = chutes_modelo.assign(xG=xG)
        chutes_40= chutes_modelo.sample(n=40, random_state=42)
        fig,ax=plt.subplots(num=1)
        ax.plot(chutes_40['Angulo']*180/np.pi, chutes_40['Gol'], linestyle='none', 
                marker= '.', markerSize= 12, color='black')
        ax.plot(x, y, linestyle='solid', color='black')
        ax.plot(x, 1-y, linestyle='solid', color='black')
        loglikelihood=0
        for item, chute in chutes_40.iterrows():
            ang=chute['Angulo']*180/np.pi
            if chute['Gol']==1:
                loglikelihood=loglikelihood+np.log(chute['xG'])
                ax.plot([ang,ang],[chute['Gol'],chute['xG']], color='red')
            else:
                loglikelihood=loglikelihood+np.log(1 - chute['xG'])
                ax.plot([ang,ang],[chute['Gol'],1-chute['xG']], color='blue')
    
        ax.set_ylabel('Gol marcado')
        ax.set_xlabel("Ângulo do chute (graus)")
        ax.set_yticklabels(['Não','Sim']);
        plt.ylim((-0.05,1.05))
        plt.xlim((0,80))
        plt.text(45,0.2,'Log-likelihood:') 
        plt.text(45,0.1,str(loglikelihood))
        ax.set_yticks([0,1])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if save:
            fig.savefig('Imagens/LikelihoodExemplo.pdf', dpi=None, bbox_inches="tight")
    
    elif tipo == 'likelihood otimizado angulo':
        xGprob=1/(1+np.exp(b[0] + b[1]*angulo_medio*np.pi/180)) 
        fig,ax=plt.subplots(num=1)
        ax.plot(angulo_medio, prob_gol_angulo, linestyle='none', marker= '.', markerSize= 12, color='black')
        ax.plot(angulo_medio, xGprob, linestyle='solid', color='blue')
        ax.set_ylabel('Probabilidade de marcar')
        ax.set_xlabel('Ângulo do chute (graus)')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False);
        if save:
            fig.savefig('Imagens/AjusteProbabilidadeDeGolAngulo.pdf', dpi=None, bbox_inches="tight")
        
    elif tipo == 'likelihood otimizado distancia':
        if len(b)==2:
            #predição com distância media somente
            xGprob=1/(1+np.exp(b[0] + b[1]*dist_media)) 
        else:
            #predição com distância e distância ao quadrado
            xGprob=1/(1+np.exp(b[0]+b[1]*dist_media+b[2]*pow(dist_media,2))) 
        fig,ax=plt.subplots(num=1)
        ax.plot(dist_media, prob_gol_dist, linestyle='none', marker= '.', markerSize= 12, color='black')
        ax.plot(dist_media, xGprob, linestyle='solid', color='black')
        ax.set_ylabel('Probabilidade de marcar')
        ax.set_xlabel('Distância do gol (metros)')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False);
        if save:
            fig.savefig('Imagens/ProbabilidadeDeMarcarDistancia.pdf', dpi=None, bbox_inches="tight")
        
    else:
        fig,ax=plt.subplots(num=2)
        ax.plot(angulo_medio, prob_gol_angulo, linestyle='none', marker= '.', markerSize= 12, color='black')
        ax.set_ylabel('Probabilidade de marcar')
        ax.set_xlabel("Ângulo do chute (graus)")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False);
        if save:
            fig.savefig('Imagens/ProbabilidadeDeGolPorAngulo.pdf', dpi=None, bbox_inches="tight")
    
        #Fita uma reta linear aos dados
        if tipo == 'linear':
            b=[-0.05, 1/125] # parâmetros-> Interseção e Declive
            y= b[0] + b[1]*x #Calculo de y dado x e os parâmetros
            ax.plot(x, y, linestyle='solid', color='black'); #plota reta linear
            if save:
                fig.savefig('Imagens/RegressaoLinearExemplo.pdf', dpi=None, bbox_inches="tight")
    
        #Fita uma curva sigmoide aos dados
        if tipo == 'sigmoide':
            b=[3, -3] #parâmetros
            y=1/(1+np.exp(b[0]+b[1]*x*np.pi/180)) #Calculo de y (probabilidade) dado x e os coeficientes
            ax.plot(x, y, linestyle='solid', color='black'); #plota curva sigmoide
            if save:
                fig.savefig('Imagens/SigmoideExemplo.pdf', dpi=None, bbox_inches="tight")



"""Escreve modelo regressivo para biblioteca statsmodel"""

def escreve_modelo(variaveis_preditoras= []):
    '''Função que escreve um modelo regressor para parâmetro na biblioteca statsmodels.formula.api'''
    
    modelo=''

    for v in variaveis_preditoras[:-1]:
        modelo = modelo  + v + ' + '
    modelo = modelo + variaveis_preditoras[-1]
    
    return modelo



"""Calcula xG"""

def calcula_xG(df, variaveis_preditoras, coeficientes):
    '''Função que calcula o xG dado as variáveis em variáveis preditoras e os coeficientes associados a cada uma'''
    coeficientes= -coeficientes
    predicao=coeficientes[0]
    for indice, variavel in enumerate(variaveis_preditoras):
        predicao=predicao + coeficientes[indice+1] * df[variavel]
    xG = 1/(1+np.exp(predicao)) 
    return float(xG)

"""Indica se um determinado chute foi ou não gol utilizando a função calcula xG e de acordo com um threshold que possui 0.5 como valor padrão."""

def prediz_gol(df, threshold= 0.5):
    '''Função que retorna a predição se foi gol ou não de finalizações em um dataframe'''
    
    df= df.assign(predicao= df['xG'].apply(lambda xg: 1 if xg >= threshold else 0))
    return df['predicao'].values

"""Plota valores associados de especificidade e sensitividade do modelo por threshold"""

def plot_metricas_e_thresh(df, y_true, lista_thresh, save= False):
    
    colors= ['orange', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    colors= colors[:len(lista_thresh)]
    
    
    fig,ax=plt.subplots(num=1)
    for thresh in lista_thresh:
        
        #predições
        y_pred= prediz_gol(df, threshold= thresh)

        #Erros e acertos
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

        #Acetos não gol
        especificidade = (tn / (tn+fp)).round(3)#*100

        #Acertos gol
        precisao= precision_score(y_true, y_pred).round(3)#*100

        #Scatterplot acertos não gol por acertos gol
        ax.scatter(x= especificidade, y= precisao, marker= 'o', 
        label= f'Threshold:{str(thresh*100)[:4]}%, Especificidade: {str(especificidade*100)[:4]}%, Sensitividade: {str(precisao*100)[:4]}%',
    linewidth=5, color= colors[lista_thresh.index(thresh)])

        #Linha que demarca onde a taxa de acertos de gols e não gols seriam iguais
        ax.plot(np.arange(start=0, stop=1, step=0.01), 
                 np.arange(start=0, stop=1, step=0.01),
              linewidth=2, linestyle='-')
    
    ax.legend(fontsize=  'x-small')

    ax.set_xlabel('Verdadeiro não Gol - Especificidade')

    ax.set_ylabel('Verdadeiro Gol - Sensitividade')

    ax.set_title('Acertos')
    plt.show()

    #Salva a figura gerada
    if save:
        fig.savefig('Imagens/taxaAcertosPorThreshold.pdf', dpi=None, bbox_inches="tight")
