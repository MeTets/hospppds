from flask import Flask, render_template, redirect, url_for, request
import db

app = Flask(__name__)

queri = db.dbconn()

@app.route('/turma/<sla>', methods=['GET', 'POST'])
def turma(sla):
    if request.method == 'GET':
        slastr = str(sla)
        responseAlunos = queri.conexao(f"SELECT cod_aluno, nome_aluno FROM Alunos WHERE cod_turma = {slastr}")
        responseProfs = queri.conexao(f"SELECT P.nome_prof, P.cod_prof FROM Professores P INNER JOIN Prof_Turma_Disc PT ON (P.cod_prof = PT.cod_prof) WHERE PT.cod_turma = {sla}")
        return render_template("turma.html", numeroSala=sla, responseProfs=responseProfs, responseAlunos=responseAlunos)
    elif request.method == 'POST':
        faltas = request.args('horario')
        print(faltas)
        return render_template("turma.html", faltas=faltas)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        sala = request.form['valorSala']
        return redirect(url_for("turma", sla=sala))
    else:
        response = queri.conexao("SELECT COUNT(cod_aluno) FROM Alunos WHERE cod_turma = 1;")
        abc = 0
        for row in response:
            abc = row.count
        return render_template("index.html", nalunos = abc)

if __name__ == "__main__":
    app.run()
