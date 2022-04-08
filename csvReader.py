import csv
from fpdf import FPDF
import requests
from datetime import date, datetime, timedelta


class Task:
    def __init__(self, subject, description, us, assigned, status, init_date, fin_date, hours):
        self.hours = hours
        self.fin_date = fin_date
        self.init_date = init_date
        self.status = status
        self.assigned = assigned
        self.description = description
        self.subject = subject
        self.us = us


# 0- Tasks, 1- User Stories
modo = 0
today = date.today()
todayF = today.strftime("%d-%b-%Y")  # ddmmaaaa
if modo == 0:
    filename = "Tareas" + " - " + str(todayF)
    url = 'https://api.taiga.io/api/v1/tasks/csv?uuid=7db9148a134947d89c13468473c193a0'
else:
    filename = "Historias de usuario" + " - " + str(todayF)
    url = 'https://api.taiga.io/api/v1/userstories/csv?uuid=c5994f0ac74c46bd84adb5e061546f86'

path = 'C:/Users/dalares/Downloads/' # Ruta donde descargamos y creamos el .pdf
r = requests.get(url, allow_redirects=True)  # download .csv from Taiga's URL and save it in path
open(path + filename + '.csv', 'wb').write(r.content)

# open pdf and set styles
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=15)

# open weekly pdf
pdfWeek = FPDF()
pdfWeek.add_page()
pdfWeek.set_font("Arial", size=15)

lista = []
countAsalomon = 0
cHorasAsalomon = 0
textAsalomon = ""
countAicucu = 0
cHorasAicucu= 0
textAicucu=""
countJlavina = 0
textJlavina=""
cHorasJlavina = 0
with open(path + filename + '.csv', encoding="latin-1") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    # loop all files and print pdf
    for row in csv_reader:
        if line_count == 0:
            pdf.cell(200, 10, txt=filename, ln=line_count, align='C')
            pdfWeek.cell(200, 10, txt=filename, ln=line_count, align='C')
            line_count += 1
        else:
            t = Task(row[2], row[3], row[4], row[12], row[13], row[23], row[25], row[28])
            pdf.cell(200, 10, txt='', ln=line_count, align='L')
            pdf.cell(200, 10, txt=str(line_count), ln=line_count, align='L')

            pdf.set_font("Arial", 'B', 15)
            pdf.multi_cell(200, 10, txt=f'{t.assigned} - {t.subject}', align='L')
            pdf.set_font("Arial", size=15)

            pdf.multi_cell(200, 10, txt=str(t.description), align='L')
            pdf.cell(200, 10, txt=f'--> STATUS: {t.status}', ln=line_count, align='L')
            pdf.cell(200, 10, txt=f'--> INIT DATE: {t.init_date[0:19]}', ln=line_count, align='L')
            pdf.cell(200, 10, txt=f'--> END DATE: {t.fin_date[0:19]}', ln=line_count, align='L')

            h = '--> HOURS: 8' if t.hours == '' else f'--> HOURS: {t.hours}'
            pdf.cell(200, 10, txt=h, ln=line_count, align='L')
            pdf.cell(200, 10, txt=f'--> USER STORY: {t.us}', ln=line_count, align='L')
            line_count += 1

            d = datetime.today() - timedelta(days=5)  # weekly pdf with sysdate -5 days
            date_time_str = t.init_date[2:19]
            date_time_obj = datetime.strptime(date_time_str, '%y-%m-%d %H:%M:%S')
            if date_time_obj > d:
                pdfWeek.cell(200, 10, txt='', ln=line_count, align='L')
                pdfWeek.cell(200, 10, txt=str(line_count), ln=line_count, align='L')

                pdfWeek.set_font("Arial", 'B', 15)
                pdfWeek.multi_cell(200, 10, txt=f'{t.assigned} - {t.subject}', align='L')
                pdfWeek.set_font("Arial", size=15)

                pdfWeek.multi_cell(200, 10, txt=str(t.description), align='L')
                pdfWeek.cell(200, 10, txt=f'--> STATUS: {t.status}', ln=line_count, align='L')
                pdfWeek.cell(200, 10, txt=f'--> INIT DATE: {t.init_date[0:19]}', ln=line_count, align='L')
                pdfWeek.cell(200, 10, txt=f'--> END DATE: {t.fin_date[0:19]}', ln=line_count, align='L')

                h = '--> HOURS: 8' if t.hours == '' else f'--> HOURS: {t.hours}'
                pdfWeek.cell(200, 10, txt=h, ln=line_count, align='L')
                pdfWeek.cell(200, 10, txt=f'--> USER STORY: {t.us}', ln=line_count, align='L')

                # Stats
                if t.assigned == 'Alessandro':
                    countAsalomon = countAsalomon + 1
                    textAsalomon = textAsalomon + t.subject
                    cHorasAsalomon = cHorasAsalomon + (float(t.hours.replace(',', '.')) if t.hours != '' else 8)

                elif t.assigned == 'Jlavina':
                    countJlavina = countJlavina + 1
                    textJlavina = textJlavina + t.subject
                    cHorasJlavina = cHorasJlavina + (float(t.hours.replace(',', '.')) if t.hours != '' else 8)

                elif t.assigned == 'Alexandru Iulian Cucu':
                    countAicucu = countAicucu + 1
                    textAicucu = textAicucu + t.subject
                    cHorasAicucu = cHorasAicucu + (float(t.hours.replace(',', '.')) if t.hours != '' else 8)

    pdfWeek.cell(200, 10, txt='', ln=line_count, align='L')
    pdfWeek.set_font("Arial", 'B', 15)
    pdfWeek.cell(200, 10, txt='ESTADISTICAS', ln=line_count, align='L')
    pdfWeek.set_font("Arial", size=15)

    pdfWeek.cell(200, 10, txt='Alessandro', ln=line_count, align='L')
    pdfWeek.cell(200, 10, txt=f'--> Nº tareas: {countAsalomon}', ln=line_count, align='L')
    pdfWeek.cell(200, 10, txt=f'--> Horas: {countAsalomon}', ln=line_count, align='L')

    pdfWeek.cell(200, 10, txt='Jlavina', ln=line_count, align='L')
    pdfWeek.cell(200, 10, txt=f'--> Nº tareas: {countJlavina}', ln=line_count, align='L')
    pdfWeek.cell(200, 10, txt=f'--> Horas: {cHorasJlavina}', ln=line_count, align='L')

    pdfWeek.cell(200, 10, txt='Aicucu', ln=line_count, align='L')
    pdfWeek.cell(200, 10, txt=f'--> Nº tareas: {countAicucu}', ln=line_count, align='L')
    pdfWeek.cell(200, 10, txt=f'--> Horas: {cHorasAicucu}', ln=line_count, align='L')

pdf.output(path + filename + ".pdf")
pdfWeek.output(path + filename + "Week.pdf")
