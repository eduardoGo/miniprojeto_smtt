import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
plt.style.use('ggplot')

def read_data():
	data =  pd.read_csv('viagens.csv')

	del data['Unnamed: 0']

	return data

def line_delay(data,top):
	
	#Dicionário no formado {num. da linha: atraso acumulado}
	lines_delay = {}

	#Dicionário no formado {num. da linha: empresa responsável}
	lines_company = {}

	#Dicionario no formato {empresa:[cor,flag para indicar se ja foi usado]}. Será útil para plotar o gráfico depois.
	companies = {}
	

	for i in range(len(data['numero_linha'].values)):
		
		current_line = str(data['numero_linha'][i])
		current_company = data['empresa'][i]
		
		#Se data['duracao_realizada'][i] é NaN, a condição do IF se torna falsa, e portanto não entra no IF.
		if data['duracao_prevista'][i] < data['duracao_realizada'][i]:

			#verifica se a chave já existe no dicionário. Se não existe, adiciona.
			if not current_line in lines_delay:
				lines_delay[current_line] = 0

			#verifica se a chave já existe no dicionário. Se não existe, adiciona.
			if not current_line in lines_company:
				lines_company[current_line] = current_company

			if not current_company in companies:
				companies[current_company] = [(random.random(),random.random(),random.random()),False] #Cor em RGB

			lines_delay[current_line] += (data['duracao_realizada'][i]-data['duracao_prevista'][i])/60


	lines_order = sorted(lines_delay,key=lines_delay.get)
	delay_order = sorted(lines_delay.values())
	company_order = [lines_company[x] for x in lines_order]

	company_order.reverse()
	lines_order.reverse()
	delay_order.reverse()

	return lines_order,delay_order,company_order,companies

def plot_delay_line(top,lines_order,delay_order,company_order,companies):

	if top == -1:
		plt.title("Atraso por linha\nIda+Volta",fontsize=20)
		top = len(lines_order)
	else:
		plt.title("Atraso por linha\nTOP "+str(top),fontsize=20)

	handles = plt.bar(lines_order[:top],delay_order[:top],width=0.5)
	
	#Loop para remover legendas duplicadas no gráfico.
	filter_handles = []
	colors = []
	for i in range(len(handles)):
		
		#Se é a primeira vez que a empresa vai apareer no gráfico, então a gente filtra, pra depois não aparecer legenda repetida
		if not companies[company_order[i]][1]:
			companies[company_order[i]][1] = True
			filter_handles.append(i)
			colors.append(companies[company_order[i]][0])
		handles[i].set_color(companies[company_order[i]][0])



	plt.ylabel("Horas",fontsize=20)
	plt.xticks(rotation='vertical')
	plt.yticks(fontsize=20)

	plt.legend(handles=[handles[x] for x in filter_handles],labels=[company_order[x] for x in filter_handles],fontsize=10)

	return colors

def plot_top_companies(top,company_order,colors):

	#dicionário no formato {empresa: quantidade de vezes que aparece no pódio}
	top_companies = {}

	for i in range(top):
		if not company_order[i] in top_companies:
			top_companies[company_order[i]] = 0

		top_companies[company_order[i]] += 1

	explode = np.zeros(len(top_companies.values()))
	explode[np.array(list(top_companies.values())).argmax()] = 0.1
	

	plt.title("Participação no pódio\npor empresa")
	plt.pie(x = top_companies.values(),labels=top_companies.keys(),autopct='%1.1f%%',
        shadow=True, startangle=90,colors=colors,explode=explode)

def review_delay(data):
	top = 15

	lines_order,delay_order,company_order,companies = line_delay(data,top)

	plt.subplot(121)
	colors = plot_delay_line(top,lines_order,delay_order,company_order,companies)

	plt.subplot(122)
	plot_top_companies(top,company_order,colors)

	plt.show()


def main():
	data = read_data()
	review_delay(data)

main()


