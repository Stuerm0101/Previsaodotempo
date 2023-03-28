import csv
import json
from urllib import request
import datetime


def lerCSV(nomeArquivo):

    csvfile = open(nomeArquivo, 'r', encoding='latin-1')
    csvreader = csv.DictReader(csvfile, delimiter=",") 
    dados = list(csvreader)

    return dados

def BuscarCidade(listacidade):
    lista = []
    dic_cidade = {
        "cidade": "",
        "pais": "",
        "lat": "",
        "lng": ""
    }
    dic_novo = {
        "cidade": "",
        "pais": "",
        "lat": "",
        "lng": ""
    }
    while True:
        lista.clear()
        cidade = str(input('Nome da cidade: (0 para sair)'))
        if cidade == '0':
            break

        for elemento in listacidade:
            if elemento["city"] == cidade:
              
                dic_cidade["cidade"] = elemento["city"]
                dic_cidade["pais"] = elemento["country"]
                dic_cidade["lat"] = elemento["lat"]
                dic_cidade["lng"] = elemento["lng"]
                lista.append(dic_cidade.copy())
                lat = dic_cidade["lat"]
                lng = dic_cidade["lng"]
                country = dic_cidade["pais"]
        if(len(lista) > 1):
            print('Escolha o país ao qual a cidade pertence:')
            for c in lista:
                print(f'{c["cidade"]}, {c["pais"]}')

            resposta = []
            escolha = str(input('Nome do país: '))
            
            for city in lista:   
                if escolha == city["pais"]:
                    country = city["pais"]
                    dic_novo["cidade"] = city["cidade"]
                    dic_novo["lat"] = city["lat"]
                    dic_novo["lng"] = city["lng"]
                    dic_novo["pais"] = city["pais"]
                    resposta.append(dic_novo)
            
            lat = resposta[0]["lat"]
            lng = resposta[0]["lng"]
        
            if len(resposta)> 0:
                print('Carregando...')
            else:
                print('Erro')
              
        reqres = request.urlopen(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=e81356d7895d143ba1a1b17178dffdab&units=metric&lang=pt_br")
        
        if (reqres and reqres.getcode() == 200):  #Testa se foi possível contactar o servidorric
            jsonResponse = json.loads(reqres.read()) #captura resposta (JSON)
            dataehora = jsonResponse['dt']
            dthconvert =datetime.datetime.fromtimestamp(dataehora)
            date_conv =datetime.datetime. fromtimestamp(jsonResponse['sys']['sunrise'])
            date_conv1=datetime.datetime. fromtimestamp(jsonResponse['sys']['sunset'])
            Temp = (jsonResponse['main']['temp'])
            feelslike = jsonResponse['main']['feels_like']
            tempo = (jsonResponse['weather'][0]['description'])
            humidade = jsonResponse['main']['humidity']
            print('======== TEMPO AGORA ========' )
            print(f'Última atualização: {dthconvert.date()} às {dthconvert.time()}')
            print(f'Cidade: {cidade}, {country}')#Achar alguma maneira de melhorar e por a cidade e o país
            print('-'*30)         
            print(f'Tempo agora: {tempo}')
            print(f'Temperatura: {Temp:0.0f}ºC')
            print(f'Sensação Térmica: {feelslike:0.0f}ºC')
            print(f'Humidade: {humidade}%')
            print(f"Nascer do Sol: {date_conv.strftime('%H:%M')}")
            print(f"Pôr do Sol: {date_conv1.strftime('%H:%M')}")
            print(f"Nebulosidade: {jsonResponse['clouds']['all']}%")     

        else:
            print (f"Não foi possível contactar o servidor. Código retornado: {reqres.getcode()}")


def buscar5dias(listacidade):
    horatest=[12,24,48]
    
    tempo_list = []
    
    while True:     
        dic_temp={
            "previsao":'',
            "temperatura":'',
            "sensação térmica":'',
            "humidade":'',
            "nebulosidade":'',
            "horario": ''}

        cidade = str(input('Nome da cidade: (0 Para sair)'))
        if cidade == '0':
            break

        lat=1

        for elemento in listacidade:
            if elemento['city'] == cidade:
                lat = elemento['lat']
                lng = elemento['lng']
                country = elemento['country']

        if lat==1:
            print("Cidade não encontrada, digite uma cidade válida.")
            continue

        reqres = request.urlopen(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lng}&lang=pt_br&appid=c14d49470d99297a2f07f062f39bf1cd&units=metric')

        horas=int(input("Quantas horas no futuro deve ser feita a previsão? 12h, 24h ou 48h?\n"))
        
        if (reqres and reqres.getcode() == 200):
            jsonResponse = json.loads(reqres.read())
        else:
            print('Não foi possível conectar ao servidor, tente novamente!')

        if horas not in horatest:
            print("Digite um valor válido")
            continue

        else:

            dividido = horas//3
            print(dividido)
            
            for cont in range(dividido):

                dic_temp["previsao"] = jsonResponse["list"][cont]["weather"][0]["description"]
                dic_temp["temperatura"] = jsonResponse["list"][cont]["main"]["temp"]
                dic_temp["max"] = jsonResponse["list"][cont]["main"]["temp_max"]
                dic_temp["min"] = jsonResponse["list"][cont]["main"]["temp_min"]
                dic_temp["sensação térmica"] = jsonResponse["list"][cont]["main"]["feels_like"]
                dic_temp["humidade"] = jsonResponse["list"][cont]["main"]["humidity"]
                dic_temp["nebulosidade"] = jsonResponse["list"][cont]["clouds"]["all"]
                dic_temp["data"] = jsonResponse["list"][cont]["dt"]
                dic_temp["horas"] = jsonResponse["list"][cont]["dt_txt"]
                
                
                tempo_list.append(dic_temp.copy())
        
        
        print('======== PREVISÃO DO TEMPO ========' )
        print(f'Cidade: {cidade}, {country}')
        for dic in tempo_list:
            print('-'*30)   
            print(f'{dic["horas"]}')  
            print(f'Previsão: {dic["previsao"]} ')
            print(f'Temperatura: {dic["temperatura"]:.0f}ºC   (Temp. Min.:{dic["min"]:.0f}°C / Temp. Máx.:{dic["max"]:.0f}°C)')
            print(f'Sensação Térmica: {dic["sensação térmica"]:.0f}ºC ')
            print(f'Humidade: {dic["humidade"]}%    Nebulosidade: {dic["nebulosidade"]}%\n')
def main():
    while True:
        optest=[1,2,3]
        print('-'*10,'Real Weather','-'*10)
        op=int(input("""
===========================================
Digite 1 para buscar o clima agora.
Digite 2 para buscar a previsão do tempo (12h/24h/48h).
Digite 3 para encerrar o programa.
===========================================
"""))
        if op not in optest:
            print("Digite um número válido")
            continue
       
    
        x = lerCSV('worldcities.csv')
        
        if op==1:    
            BuscarCidade(x)
        
        elif op==2:
            buscar5dias(x)
        
        elif op==3:
            print("O programa será encerrado.")
            break    

main()
