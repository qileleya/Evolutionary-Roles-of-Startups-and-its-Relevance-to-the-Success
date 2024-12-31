# read data
import xlrd
import xlwt

workBook = xlrd.open_workbook(r'investor-time-company-success.xls')

sheet1_content1 = workBook.sheet_by_index(0)

investor = sheet1_content1.col_values(0)
time = sheet1_content1.col_values(1)
company = sheet1_content1.col_values(2)
success = sheet1_content1.col_values(3)
date = sheet1_content1.col_values(4)

c_c = [([0] * 5) for i in range(15000)]
a = 0
for i in range(0, len(investor)):
    for j in range(i+1, len(investor)):
        if investor[i] == investor[j]:
            c_c[a][0] = company[i]
            c_c[a][1] = company[j]
            c_c[a][2] = min(time[i], time[j])
            c_c[a][3] = max(time[i], time[j])
            c_c[a][4] = max(time[i], time[j]) - min(time[i], time[j])
            a += 1
        j = j+1
    i += 1

y = [([0] * 2) for i in range(1500)]
k = 0
linshi_c = []
for i in range(len(company)):
    if company[i] not in linshi_c:
        linshi_c.append(company[i])

linshi_t = []
for j in range(len(linshi_c)):
    for i in range(len(company)):
        if company[i] == linshi_c[j]:
            linshi_t.append(time[i])
        else:
            continue
    if len(linshi_t) == 1:
        y[k][0] = 999999
    else:
        y[k][0] = max(linshi_t) - min(linshi_t)
    y[k][1] = linshi_c[j]
    k = k+1
    linshi_t.clear()

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Sheet")
for i in range(len(y)):
    for j in range(len(y[i])):
        sheet.write(i, j, y[i][j])
workbook.save("company invested.xls")
