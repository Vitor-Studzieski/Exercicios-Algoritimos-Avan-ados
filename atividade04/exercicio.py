import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

MOEDAS = [100, 50, 25, 10, 5, 1]

ROTULO = {
    100: "R$1,00",
    50:  "R$0,50",
    25:  "R$0,25",
    10:  "R$0,10",
    5:   "R$0,05",
    1:   "R$0,01",
}

def funcao_selecao(candidatos: list[int]) -> int:
    return candidatos[0]

def funcao_viabilidade(moeda: int, resto: int) -> bool:
    return moeda <= resto

def funcao_objetivo(solucao: dict[int, int]) -> int:
    return sum(solucao.values())

def funcao_solucao(resto: int) -> bool:
    return resto == 0

def troco_guloso(n: int) -> dict:
    solucao: dict[int, int] = {m: 0 for m in MOEDAS}
    candidatos = list(MOEDAS)
    resto = n
    passos = []

    while candidatos and not funcao_solucao(resto):
        moeda = funcao_selecao(candidatos)
        candidatos = candidatos[1:]

        viavel = funcao_viabilidade(moeda, resto)
        if viavel:
            quantidade = resto // moeda
            solucao[moeda] = quantidade
            resto = resto % moeda
            passos.append({
                "moeda": moeda,
                "rotulo": ROTULO[moeda],
                "viavel": True,
                "quantidade": quantidade,
                "restante": resto,
                "solucao": funcao_solucao(resto),
            })
        else:
            passos.append({
                "moeda": moeda,
                "rotulo": ROTULO[moeda],
                "viavel": False,
                "quantidade": 0,
                "restante": resto,
                "solucao": False,
            })

    return {
        "solucao": {str(k): v for k, v in solucao.items()},
        "passos": passos,
        "total_moedas": funcao_objetivo(solucao),
        "valor_brl": f"R${n / 100:.2f}".replace(".", ","),
    }

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Troco Guloso</title>
<style>
  :root {
    --bg: #f5f4f0;
    --surface: #ffffff;
    --border: #e0ddd6;
    --text: #1a1a18;
    --muted: #6b6a64;
    --accent: #2563eb;
    --accent-light: #eff6ff;
    --success: #16a34a;
    --success-light: #f0fdf4;
    --danger: #dc2626;
    --radius: 10px;
    --shadow: 0 1px 3px rgba(0,0,0,.08);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, -apple-system, sans-serif;
         background: var(--bg); color: var(--text);
         min-height: 100vh; padding: 2rem 1rem; }
  .wrapper { max-width: 820px; margin: 0 auto; }
  h1 { font-size: 1.5rem; font-weight: 600; margin-bottom: .25rem; }
  .tagline { font-size: .875rem; color: var(--muted); margin-bottom: 2rem; }

  .card { background: var(--surface); border: 1px solid var(--border);
          border-radius: var(--radius); padding: 1.25rem 1.5rem;
          box-shadow: var(--shadow); margin-bottom: 1.25rem; }
  .card-title { font-size: .68rem; font-weight: 700; letter-spacing: .1em;
                text-transform: uppercase; color: var(--muted); margin-bottom: .85rem; }

  .input-row { display: flex; gap: .75rem; align-items: flex-end; flex-wrap: wrap; }
  .field { display: flex; flex-direction: column; gap: .3rem; }
  label { font-size: .8rem; color: var(--muted); }
  input[type=number] { border: 1px solid var(--border); border-radius: 8px;
                       padding: .6rem .9rem; font-size: 1rem; width: 170px;
                       background: var(--surface); color: var(--text);
                       outline: none; transition: border-color .15s; }
  input[type=number]:focus { border-color: var(--accent); }
  .hint { font-size: .75rem; color: var(--muted); }
  button { padding: .62rem 1.5rem; border-radius: 8px; font-size: .875rem;
           font-weight: 600; cursor: pointer; border: none;
           transition: opacity .15s, transform .1s; }
  button:active { transform: scale(.97); }
  .btn-primary { background: var(--accent); color: #fff; }
  .btn-primary:hover { opacity: .87; }
  .error-msg { color: var(--danger); font-size: .83rem;
               margin-top: .5rem; display: none; }

  .comp-grid { display: grid;
               grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
               gap: .75rem; margin-bottom: 1.25rem; }
  .comp-item { background: var(--surface); border: 1px solid var(--border);
               border-radius: var(--radius); padding: .9rem 1rem;
               box-shadow: var(--shadow); }
  .comp-tag { font-size: .65rem; font-weight: 700; letter-spacing: .1em;
              text-transform: uppercase; color: var(--accent); margin-bottom: .4rem; }
  .comp-desc { font-size: .82rem; color: var(--text); line-height: 1.5; }
  .comp-desc code { background: var(--accent-light); color: var(--accent);
                    border-radius: 4px; padding: 1px 5px; font-size: .78rem; }

  table { width: 100%; border-collapse: collapse; font-size: .84rem; }
  thead th { text-align: left; font-size: .68rem; font-weight: 700;
             letter-spacing: .07em; text-transform: uppercase; color: var(--muted);
             padding: .5rem .75rem; border-bottom: 1px solid var(--border); }
  tbody td { padding: .65rem .75rem; border-bottom: 1px solid var(--border); }
  tbody tr:last-child td { border-bottom: none; }
  tr.row-ok    td { background: var(--success-light); }
  tr.row-skip  td { color: var(--muted); }
  tr.row-solved td { background: var(--success-light); font-weight: 600; }
  .badge { display: inline-block; font-size: .72rem; font-weight: 700;
           padding: 2px 9px; border-radius: 20px; }
  .badge-sim    { background: var(--success-light); color: var(--success); }
  .badge-nao    { background: var(--border); color: var(--muted); }
  .badge-solved { background: var(--success-light); color: var(--success); }

  .coins-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
  .coin { display: flex; flex-direction: column; align-items: center; gap: .35rem; }
  .coin-circle { width: 54px; height: 54px; border-radius: 50%;
                 display: flex; align-items: center; justify-content: center;
                 font-size: 1.15rem; font-weight: 700; border: 2.5px solid; }
  .coin-label { font-size: .7rem; color: var(--muted); }
  .coin-zero .coin-circle { opacity: .22; }

  .totals { display: flex; gap: 2rem; flex-wrap: wrap; }
  .total-item { font-size: .875rem; color: var(--muted); }
  .total-item strong { color: var(--text); font-weight: 700; font-size: 1rem; }
  #results { display: none; }
  hr.sep { border: none; border-top: 1px solid var(--border); margin: .85rem 0; }
</style>
</head>
<body>
<div class="wrapper">
  <h1>Problema do Troco &mdash; Algoritmo Guloso</h1>
  <p class="tagline">Modelagem com os 5 componentes da estratégia gulosa</p>

  <div class="card">
    <div class="card-title">Entrada</div>
    <div class="input-row">
      <div class="field">
        <label for="valor">Valor em centavos</label>
        <input type="number" id="valor" min="1" max="99999" value="289">
        <span class="hint">Ex: 289 &rarr; R$2,89 &nbsp;|&nbsp; 100 &rarr; R$1,00</span>
      </div>
      <button class="btn-primary" onclick="calcular()">Calcular troco</button>
    </div>
    <div class="error-msg" id="erro"></div>
  </div>

  <div class="comp-grid">
    <div class="comp-item">
      <div class="comp-tag">1 &middot; Candidatos</div>
      <div class="comp-desc">Moedas disponíveis:<br><code>{100, 50, 25, 10, 5, 1}</code></div>
    </div>
    <div class="comp-item">
      <div class="comp-tag">2 &middot; Seleção</div>
      <div class="comp-desc">Escolhe a <strong>maior moeda</strong> &le; valor restante a cada passo</div>
    </div>
    <div class="comp-item">
      <div class="comp-tag">3 &middot; Viabilidade</div>
      <div class="comp-desc">Moeda é viável se <code>moeda &le; resto</code></div>
    </div>
    <div class="comp-item">
      <div class="comp-tag">4 &middot; Objetivo</div>
      <div class="comp-desc">Minimizar o <strong>total</strong> de moedas utilizadas</div>
    </div>
    <div class="comp-item" style="grid-column:1/-1">
      <div class="comp-tag">5 &middot; Solução</div>
      <div class="comp-desc">Solução completa quando <code>resto = 0</code></div>
    </div>
  </div>

  <div id="results">
    <div class="card">
      <div class="card-title">Execução passo a passo</div>
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Moeda selecionada</th>
            <th>Viável?</th>
            <th>Qtd usada</th>
            <th>Restante após</th>
            <th>Solução?</th>
          </tr>
        </thead>
        <tbody id="tabela-passos"></tbody>
      </table>
    </div>

    <div class="card">
      <div class="card-title">Resultado final</div>
      <div class="coins-row" id="coins-row"></div>
      <hr class="sep">
      <div class="totals">
        <div class="total-item">Total de moedas: <strong id="total-qtd">—</strong></div>
        <div class="total-item">Valor: <strong id="total-valor">—</strong></div>
      </div>
    </div>
  </div>
</div>

<script>
const COIN_COLORS = {
  '100': {color:'#92400e', bg:'#fef3c7'},
  '50':  {color:'#374151', bg:'#f3f4f6'},
  '25':  {color:'#374151', bg:'#f3f4f6'},
  '10':  {color:'#1e40af', bg:'#dbeafe'},
  '5':   {color:'#1e40af', bg:'#dbeafe'},
  '1':   {color:'#166534', bg:'#dcfce7'},
};
const ROTULOS = {
  '100':'R$1,00','50':'R$0,50','25':'R$0,25',
  '10':'R$0,10','5':'R$0,05','1':'R$0,01'
};
const MOEDAS = ['100','50','25','10','5','1'];

async function calcular() {
  const val = document.getElementById('valor').value.trim();
  const erro = document.getElementById('erro');
  erro.style.display = 'none';
  if (!val || isNaN(val) || parseInt(val) < 1 || parseInt(val) > 99999) {
    erro.textContent = 'Insira um valor inteiro entre 1 e 99.999 centavos.';
    erro.style.display = 'block';
    return;
  }
  const res = await fetch('/calcular?n=' + parseInt(val));
  const data = await res.json();
  renderizar(data);
}

function renderizar(data) {
  const tbody = document.getElementById('tabela-passos');
  tbody.innerHTML = '';
  let passo = 0;
  data.passos.forEach(p => {
    const tr = document.createElement('tr');
    tr.className = p.solucao ? 'row-solved' : (p.viavel ? 'row-ok' : 'row-skip');
    const num  = p.viavel ? (++passo) : '&mdash;';
    const qtd  = p.viavel ? p.quantidade : '&mdash;';
    const rest = p.restante + '&cent;';
    const sol  = p.solucao
      ? '<span class="badge badge-solved">&#10003; Sim</span>' : '&mdash;';
    const vBadge = p.viavel
      ? '<span class="badge badge-sim">Sim</span>'
      : '<span class="badge badge-nao">N&atilde;o</span>';
    tr.innerHTML = `<td>${num}</td><td>${p.moeda}&cent; (${p.rotulo})</td>
                    <td>${vBadge}</td><td>${qtd}</td><td>${rest}</td><td>${sol}</td>`;
    tbody.appendChild(tr);
  });

  const row = document.getElementById('coins-row');
  row.innerHTML = '';
  MOEDAS.forEach(m => {
    const qtd = data.solucao[m] || 0;
    const c = COIN_COLORS[m];
    const div = document.createElement('div');
    div.className = 'coin' + (qtd === 0 ? ' coin-zero' : '');
    div.innerHTML = `
      <div class="coin-circle"
           style="color:${c.color};border-color:${c.color};background:${c.bg}">${qtd}</div>
      <div class="coin-label">${ROTULOS[m]}</div>`;
    row.appendChild(div);
  });

  document.getElementById('total-qtd').textContent = data.total_moedas;
  document.getElementById('total-valor').textContent = data.valor_brl;
  document.getElementById('results').style.display = 'block';
  document.getElementById('results').scrollIntoView({behavior:'smooth', block:'start'});
}

document.getElementById('valor').addEventListener('keydown', e => {
  if (e.key === 'Enter') calcular();
});
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/calcular":
            params = parse_qs(parsed.query)
            try:
                n = int(params["n"][0])
                if n < 1 or n > 99999:
                    raise ValueError
                resultado = troco_guloso(n)
                body = json.dumps(resultado).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
            except (KeyError, ValueError, IndexError):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"erro": "valor invalido"}')
        else:
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

if __name__ == "__main__":
    PORT = 8765
    server = HTTPServer(("localhost", PORT), Handler)

    url = f"http://localhost:{PORT}"
    print("=" * 50)
    print("  TROCO GULOSO — Interface Gráfica")
    print("=" * 50)
    print(f"  Servidor iniciado em: {url}")
    print("  Abrindo o navegador automaticamente...")
    print("  Pressione Ctrl+C para encerrar.")
    print("=" * 50)

    threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Servidor encerrado.")
        server.server_close()