from flask import Flask, render_template_string, request, jsonify
import datetime
import socket
import json
import os

app = Flask(__name__)
RESPUESTAS_FILE = "respuestas.json"

def cargar_respuestas():
    if os.path.exists(RESPUESTAS_FILE):
        with open(RESPUESTAS_FILE) as f:
            return json.load(f)
    return []

def guardar_respuesta(entrada):
    data = cargar_respuestas()
    data.append(entrada)
    with open(RESPUESTAS_FILE, "w") as f:
        json.dump(data, f)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# ─────────────────────────────────────────────
#  PÁGINA PRINCIPAL (ella la ve en su celular)
# ─────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Para ti 💌</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }

        :root {
            --pink: #ff6b9d;
            --pink-light: #ffb3d0;
            --dark: #0f0a1e;
            --dark2: #1a1035;
            --glass: rgba(255,255,255,0.06);
            --glass-border: rgba(255,255,255,0.13);
        }

        body {
            font-family: 'Lato', sans-serif;
            background: var(--dark);
            color: #fff;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* ── Fondo de estrellas ── */
        #stars {
            position: fixed; inset: 0; z-index: 0; pointer-events: none;
        }
        .star {
            position: absolute; background: white; border-radius: 50%;
            animation: twinkle var(--d) ease-in-out infinite;
        }
        @keyframes twinkle {
            0%,100% { opacity:.15; transform:scale(1); }
            50%      { opacity:1;   transform:scale(1.5); }
        }

        /* ── Corazones flotantes ── */
        #hearts {
            position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
        }
        .fheart {
            position: absolute; bottom:-60px;
            animation: floatUp var(--d2) linear infinite; opacity:0;
        }
        @keyframes floatUp {
            0%   { bottom:-60px; opacity:0; transform:translateX(0); }
            10%  { opacity:.9; }
            90%  { opacity:.3; }
            100% { bottom:110vh; opacity:0; transform:translateX(var(--drift)); }
        }

        /* ── Contenido ── */
        .page { position:relative; z-index:10; padding: 24px 16px 60px; max-width: 500px; margin: auto; }

        /* ── Hero ── */
        .hero {
            text-align: center;
            padding: 36px 20px 28px;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 28px;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 60px rgba(0,0,0,.5), 0 0 60px rgba(255,107,157,.1);
            margin-bottom: 20px;
            animation: fadeUp .9s ease forwards;
        }
        @keyframes fadeUp {
            from { opacity:0; transform:translateY(30px); }
            to   { opacity:1; transform:translateY(0); }
        }

        .envelope { font-size:2.8rem; display:block; margin-bottom:10px;
            animation: pulse 2s ease-in-out infinite; }
        @keyframes pulse {
            0%,100% { transform:scale(1); } 50% { transform:scale(1.12); }
        }

        .label {
            font-weight:300; font-size:.72rem; letter-spacing:4px;
            text-transform:uppercase; color:var(--pink-light); opacity:.7;
            margin-bottom:12px; display:block;
        }
        h1 {
            font-family:'Playfair Display', serif;
            font-size:2rem; line-height:1.25;
            margin-bottom:6px;
        }
        h1 em { color:var(--pink); font-style:italic; }

        .divider {
            width:50px; height:2px; margin:16px auto;
            background:linear-gradient(90deg,transparent,var(--pink),transparent);
        }

        .hero-text { font-size:.98rem; color:rgba(255,255,255,.8); line-height:1.7; }

        /* ── Sushi gallery ── */
        .section {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            backdrop-filter: blur(16px);
            overflow: hidden;
            margin-bottom: 20px;
            animation: fadeUp .9s ease .15s both;
            box-shadow: 0 10px 40px rgba(0,0,0,.4);
        }

        .section-label {
            padding: 14px 20px 0;
            font-size:.7rem; letter-spacing:3px; text-transform:uppercase;
            color:var(--pink-light); opacity:.7;
        }
        .section-title {
            padding: 4px 20px 14px;
            font-family:'Playfair Display', serif;
            font-size:1.3rem;
        }

        .sushi-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3px;
        }
        .sushi-grid img {
            width:100%; aspect-ratio:1; object-fit:cover;
            display:block; transition:.3s;
        }
        .sushi-grid img:hover { filter:brightness(1.1) saturate(1.2); }
        .sushi-grid img:first-child {
            grid-column: 1/-1;
            aspect-ratio: 16/9;
        }

        /* ── Trailer ── */
        .video-wrap {
            position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;
        }
        .video-wrap iframe {
            position:absolute; inset:0; width:100%; height:100%;
            border:none;
        }

        /* ── Botones de respuesta ── */
        .cta-section {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            backdrop-filter: blur(16px);
            padding: 28px 24px 32px;
            text-align: center;
            animation: fadeUp .9s ease .3s both;
            box-shadow: 0 10px 40px rgba(0,0,0,.4);
        }
        .question {
            font-family:'Playfair Display', serif;
            font-style:italic; font-size:1.25rem;
            margin-bottom:22px; color:rgba(255,255,255,.9);
        }
        .btns { display:flex; flex-direction:column; gap:12px; }
        .btn {
            padding:16px 24px; border:none; border-radius:50px;
            font-family:'Lato', sans-serif; font-size:1rem;
            cursor:pointer; transition:.25s; width:100%;
        }
        .btn-yes {
            background:linear-gradient(135deg,#ff4d8d,#ff85b5);
            color:#fff;
            box-shadow:0 8px 24px rgba(255,77,141,.4);
        }
        .btn-yes:active { transform:scale(.97); }
        .btn-no {
            background:rgba(255,255,255,.07);
            color:rgba(255,255,255,.7);
            border:1px solid rgba(255,255,255,.15);
        }
        .btn-no:active { transform:scale(.97); }

        .amor-note {
            margin-top:20px; font-size:.78rem;
            color:rgba(255,255,255,.28); letter-spacing:1px;
        }

        /* ── Pantalla de respuesta ── */
        #gracias-screen {
            display:none;
            position:fixed; inset:0; z-index:100;
            background:var(--dark);
            flex-direction:column; align-items:center; justify-content:center;
            text-align:center; padding:30px;
        }
        #gracias-screen.show { display:flex; animation:fadeUp .6s ease; }
        .big-heart { font-size:5rem; animation:pulse 1.5s ease-in-out infinite; }
        #gracias-screen h2 {
            font-family:'Playfair Display', serif; font-size:2rem; margin:18px 0 10px;
        }
        #gracias-screen p { color:rgba(255,255,255,.75); font-size:1rem; line-height:1.7; }
        .dia-chip {
            margin-top:18px; display:inline-block;
            background:linear-gradient(135deg,#ff4d8d,#ff85b5);
            padding:10px 28px; border-radius:50px;
            font-size:1rem; box-shadow:0 6px 20px rgba(255,77,141,.4);
        }
        #confetti-layer { position:fixed; inset:0; pointer-events:none; z-index:101; }
        .cp {
            position:absolute; border-radius:2px;
            animation:cf var(--d3) linear infinite; opacity:0;
        }
        @keyframes cf {
            0%   { top:-20px; opacity:1;  transform:translateX(0) rotate(0deg); }
            100% { top:110vh; opacity:0; transform:translateX(var(--drift)) rotate(var(--spin)); }
        }
    </style>
</head>
<body>

<div id="stars"></div>
<div id="hearts"></div>
<div id="confetti-layer"></div>

<!-- PANTALLA DE GRACIAS (aparece al aceptar) -->
<div id="gracias-screen">
    <span class="big-heart">🎉</span>
    <h2>¡Sabía que dirías que sí! 💖</h2>
    <p>El <strong id="dia-elegido"></strong> te espero,<br>mi niña bonita 🥰</p>
    <div class="dia-chip" id="dia-chip"></div>
    <p style="margin-top:22px;opacity:.5;font-size:.8rem;">Te amo muchísimo ♥</p>
</div>

<!-- CONTENIDO PRINCIPAL -->
<div class="page">

    <!-- HERO -->
    <div class="hero">
        <span class="envelope">💌</span>
        <span class="label">para mi niña bonita</span>
        <h1>Hola,<br><em>mi amor</em> 😘</h1>
        <div class="divider"></div>
        <p class="hero-text">
            Quiero salir contigo esta noche.<br>
            Sushi, cine, y tú —<br>
            no necesito nada más.
        </p>
    </div>

    <!-- POEMA -->
    <div class="section" style="animation-delay:.05s; text-align:center;">
        <div style="padding:28px 26px 30px;">
            <p class="section-label" style="margin-bottom:14px;">para ti</p>
            <p style="
                font-family:'Playfair Display', serif;
                font-style:italic;
                font-size:1.05rem;
                color:rgba(255,255,255,.88);
                line-height:1.95;
            ">
                Me pierdo en tus ojos<br>
                cada vez que me miras,<br>
                como si ahí adentro<br>
                viviera todo lo que quiero.<br><br>
                Tu sonrisa me desarma,<br>
                aparece y ya no puedo<br>
                pensar en nada más.<br><br>
                Y tu piel, suave como la seda,<br>
                me recuerda que hay cosas<br>
                que no se describen —<br>
                solo se sienten.<br><br>
                Eso eres tú para mí.
            </p>
            <div style="width:40px;height:1px;background:rgba(255,107,157,.4);margin:20px auto 0;"></div>
        </div>
    </div>

    <!-- SUSHI -->
    <div class="section">
        <p class="section-label">Primero</p>
        <p class="section-title">🍣 Cena de sushi juntos</p>
        <div class="sushi-grid">
            <img src="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=800&q=80" alt="sushi">
            <img src="https://images.unsplash.com/photo-1534482421-64566f976cfa?auto=format&fit=crop&w=400&q=80" alt="sushi rolls">
            <img src="https://images.unsplash.com/photo-1559410545-0bdcd187e0a6?auto=format&fit=crop&w=400&q=80" alt="sushi nigiri">
        </div>
    </div>

    <!-- TRAILER -->
    <div class="section" style="animation-delay:.2s">
        <p class="section-label">Después</p>
        <p class="section-title">🎬 Vamos al cine</p>
        <div class="video-wrap">
            <iframe
                src="https://www.youtube.com/embed/rZ6xn57p4J0?rel=0&modestbranding=1"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>
    </div>

    <!-- CTA -->
    <div class="cta-section">
        <p class="question">¿Cuándo puedes, mi vida?</p>
        <form id="form-respuesta">
            <div class="btns">
                <button type="button" class="btn btn-yes" onclick="aceptar('Hoy viernes')">
                    Hoy mismo 🌸 Viernes
                </button>
                <button type="button" class="btn btn-yes" onclick="aceptar('Domingo')">
                    El domingo 🌙
                </button>
                <button type="button" class="btn btn-no" onclick="aceptar('Otro día')">
                    Hablamos de la fecha 💬
                </button>
            </div>
        </form>
        <p class="amor-note">Con todo mi amor ♥</p>
    </div>

</div>

<script>
// ── Estrellas ──
const stEl = document.getElementById('stars');
for (let i=0;i<130;i++){
    const s=document.createElement('div');
    s.className='star';
    const sz=Math.random()*2.5+.5;
    Object.assign(s.style,{
        width:sz+'px',height:sz+'px',
        top:Math.random()*100+'%',left:Math.random()*100+'%',
        '--d':(Math.random()*3+2)+'s',
        animationDelay:(Math.random()*5)+'s'
    });
    stEl.appendChild(s);
}

// ── Corazones ──
const hEl=document.getElementById('hearts');
const emojis=['💖','💗','💕','🌸','✨','💓'];
for(let i=0;i<20;i++){
    const h=document.createElement('div');
    h.className='fheart';
    h.textContent=emojis[Math.floor(Math.random()*emojis.length)];
    Object.assign(h.style,{
        left:Math.random()*100+'%',
        fontSize:(Math.random()*.8+.7)+'rem',
        '--d2':(Math.random()*8+6)+'s',
        '--drift':((Math.random()-.5)*180)+'px',
        animationDelay:(Math.random()*10)+'s'
    });
    hEl.appendChild(h);
}

// ── Confeti ──
function lanzarConfeti(){
    const cl=document.getElementById('confetti-layer');
    const colors=['#ff7aa8','#ffd6e7','#ff4d8d','#ffb347','#a8edea','#fff','#c3b1e1'];
    for(let i=0;i<100;i++){
        const c=document.createElement('div');
        c.className='cp';
        Object.assign(c.style,{
            left:Math.random()*100+'%',
            background:colors[Math.floor(Math.random()*colors.length)],
            width:(Math.random()*8+5)+'px',
            height:(Math.random()*10+7)+'px',
            borderRadius:Math.random()>.5?'50%':'2px',
            '--d3':(Math.random()*3+2)+'s',
            '--drift':((Math.random()-.5)*400)+'px',
            '--spin':((Math.random()*720)-360)+'deg',
            animationDelay:(Math.random()*2.5)+'s'
        });
        cl.appendChild(c);
    }
}

// ── Aceptar ──
function aceptar(dia){
    // Enviar al servidor
    fetch('/', {
        method:'POST',
        headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body:'dia='+encodeURIComponent(dia)
    });

    // Mostrar pantalla de gracias
    document.getElementById('dia-elegido').textContent=dia;
    document.getElementById('dia-chip').textContent=dia+' confirmado ✓';
    const screen=document.getElementById('gracias-screen');
    screen.classList.add('show');
    lanzarConfeti();
}
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────
#  PÁGINA DE ADMIN (tú la ves para saber si respondió)
# ─────────────────────────────────────────────
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin — ¿Respondió?</title>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Lato',sans-serif;
            background:#0f0a1e; color:#fff;
            min-height:100vh; display:flex; align-items:center; justify-content:center;
            padding:24px;
        }
        .card {
            background:rgba(255,255,255,.06);
            border:1px solid rgba(255,255,255,.13);
            border-radius:24px; padding:40px 32px;
            max-width:440px; width:100%;
            box-shadow:0 20px 60px rgba(0,0,0,.5);
            text-align:center;
        }
        .status-icon { font-size:3.5rem; margin-bottom:12px; display:block; }
        h2 { font-size:1.5rem; margin-bottom:8px; }
        .sub { color:rgba(255,255,255,.5); font-size:.9rem; margin-bottom:28px; }

        #estado {
            padding:18px 24px; border-radius:16px;
            font-size:1.1rem; margin-bottom:20px;
            transition:.4s;
        }
        .esperando {
            background:rgba(255,200,0,.08);
            border:1px solid rgba(255,200,0,.25);
            color:#ffd60a;
        }
        .respondio {
            background:rgba(80,200,120,.12);
            border:1px solid rgba(80,200,120,.35);
            color:#4cff8a;
        }

        .respuesta-detalle {
            display:none;
            background:rgba(255,107,157,.08);
            border:1px solid rgba(255,107,157,.25);
            border-radius:14px; padding:16px 20px;
            text-align:left; margin-bottom:20px;
        }
        .respuesta-detalle.show { display:block; }
        .respuesta-detalle .row { display:flex; justify-content:space-between; padding:6px 0;
            border-bottom:1px solid rgba(255,255,255,.07); font-size:.92rem; }
        .respuesta-detalle .row:last-child { border-bottom:none; }
        .respuesta-detalle .key { color:rgba(255,255,255,.5); }
        .respuesta-detalle .val { color:#ffd6e7; font-weight:700; }

        .link-box {
            background:rgba(255,255,255,.04);
            border:1px solid rgba(255,255,255,.1);
            border-radius:12px; padding:14px 18px;
            font-size:.82rem; color:rgba(255,255,255,.55);
            word-break:break-all; text-align:left;
        }
        .link-box strong { color:rgba(255,255,255,.8); display:block; margin-bottom:6px; font-size:.8rem; letter-spacing:1px; text-transform:uppercase; }
        .link-url { color:#80c8ff; }

        .dot {
            display:inline-block; width:9px; height:9px; border-radius:50%;
            background:#ffd60a; margin-right:8px;
            animation:blink 1.2s ease-in-out infinite;
        }
        .dot.verde { background:#4cff8a; animation:none; }
        @keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.2;} }
    </style>
</head>
<body>
<div class="card">
    <span class="status-icon" id="icono">⏳</span>
    <h2 id="titulo">Esperando respuesta…</h2>
    <p class="sub">La página revisa automáticamente cada 3 segundos.</p>

    <div id="estado" class="esperando">
        <span class="dot" id="dot"></span>
        <span id="estado-texto">Sin respuesta todavía</span>
    </div>

    <div class="respuesta-detalle" id="detalle">
        <div class="row"><span class="key">Eligió</span><span class="val" id="val-dia">—</span></div>
        <div class="row"><span class="key">Hora</span><span class="val" id="val-hora">—</span></div>
    </div>

    <div class="link-box">
        <strong>Enlace para compartir con ella</strong>
        Conéctala a tu misma red WiFi y mándale este enlace:<br><br>
        <span class="link-url" id="link-local">Cargando…</span>
    </div>
</div>

<script>
    // Mostrar la IP local para compartir
    document.getElementById('link-local').textContent = 'http://{{ ip }}:5000/';

    let yaNotifico = false;

    async function verificar(){
        try {
            const r = await fetch('/api/estado');
            const data = await r.json();

            if(data.respondio){
                const resp = data.ultima;
                document.getElementById('icono').textContent = '🎉';
                document.getElementById('titulo').textContent = '¡Respondió! 💖';
                document.getElementById('estado').className = 'respondio';
                document.getElementById('dot').className = 'dot verde';
                document.getElementById('estado-texto').textContent = '✓ ¡Ya contestó!';
                document.getElementById('val-dia').textContent = resp.dia;
                document.getElementById('val-hora').textContent = resp.fecha;
                document.getElementById('detalle').classList.add('show');

                if(!yaNotifico){
                    yaNotifico = true;
                    // Notificación del navegador
                    if(Notification.permission === 'granted'){
                        new Notification('¡Respondió! 💖', { body: 'Eligió: ' + resp.dia });
                    }
                }
            }
        } catch(e) {}
    }

    // Pedir permiso de notificación
    if(Notification.permission !== 'granted' && Notification.permission !== 'denied'){
        Notification.requestPermission();
    }

    verificar();
    setInterval(verificar, 3000);
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────
#  RUTAS
# ─────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def invitacion():
    if request.method == "POST":
        dia = request.form.get("dia", "—")
        fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        guardar_respuesta({"dia": dia, "fecha": fecha})
        return ("", 204)   # respuesta vacía — la animación la maneja el JS
    return render_template_string(HTML)

@app.route("/api/estado")
def api_estado():
    data = cargar_respuestas()
    if data:
        return jsonify({"respondio": True, "ultima": data[-1]})
    return jsonify({"respondio": False})

@app.route("/admin")
def admin():
    ip = get_local_ip()
    return render_template_string(ADMIN_HTML, ip=ip)

if __name__ == "__main__":
    ip = get_local_ip()
    print("\n" + "─"*50)
    print(f"  Invitación:  http://{ip}:5000/")
    print(f"  Admin:       http://127.0.0.1:5000/admin")
    print("─"*50 + "\n")
    app.run(host="0.0.0.0", debug=True)
