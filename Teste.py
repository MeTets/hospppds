from flask import Flask, render_template, redirect, url_for, request
import db
import Alunos

app = Flask(__name__)

queri = db.dbconn()

@app.route('/turma/<sla>', methods=['GET', 'POST'])
def turma(sla):
    if request.method == 'GET':
        slastr = str(sla)
        responseAlunos = queri.conexao(f"SELECT cod_aluno, nome_aluno FROM Alunos WHERE cod_turma = {slastr};")
        responseProfs = queri.conexao(f"SELECT P.nome_prof, P.cod_prof FROM Professores P INNER JOIN Prof_Turma_Disc PT ON (P.cod_prof = PT.cod_prof) WHERE PT.cod_turma = {sla};")
        return render_template("turma.html", numeroSala=sla, responseProfs=responseProfs, responseAlunos=responseAlunos)
    
    elif request.method == 'POST':
        faltasCod = request.form.getlist('codigoAluno')
        faltas1 = request.form.getlist('horario1')
        faltas2 = request.form.getlist('horario2')
        profCod = request.form['profFalta']
        contador = 0
        msgErro = ""
        listaFaltas = []
        for i in range(len(faltasCod)):
            al = Alunos.Aluno(faltasCod[i], faltas1[i], faltas2[i])
            listaFaltas.append(al)
        for alunos in listaFaltas:
            if alunos.falta710 != 0 and alunos.falta1050 == 0:
                contador += 1
                pfc = int(profCod)
                aux = queri.conexaoInsert(f"INSERT INTO Faltas VALUES (CURRENT_DATE, {alunos.cod}, {pfc}, {alunos.falta710});")
                print(aux.context)
            elif alunos.falta1050 != 0 and alunos.falta710 == 0:
                contador += 1
                pfc = int(profCod)
                aux = queri.conexaoInsert(f"INSERT INTO Faltas VALUES (CURRENT_DATE, {alunos.cod}, {pfc}, {alunos.falta1050});")
                print(aux.context)
            elif alunos.falta1050 != 0 and alunos.falta710 != 0:
                msgErro = f"Você inseriu duas faltas para o aluno código {alunos.cod}. A falta do aluno {alunos.cod} não foi marcada"
            else:
                pass
        if msgErro == "":
            return render_template("faltas.html", contador = contador)
        else:
            return render_template("faltas.html", contador = contador, msgErro = msgErro)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sala = request.form['valorSala']
        return redirect(url_for("turma", sla=sala))
    else:
        response = queri.conexao("SELECT COUNT(cod_aluno) FROM Alunos GROUP BY cod_turma;")
        listaAlunos = []
        for row in response:
            listaAlunos.append(row.count)
        return render_template("index.html", response=listaAlunos)

if __name__ == "__main__":
    app.run(debug=True)
