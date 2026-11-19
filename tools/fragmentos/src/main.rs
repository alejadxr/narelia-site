use narelia_nucleo::clientes::{self, Entrada, So, TODAS};
use narelia_nucleo::formato::Idioma;
fn main() {
    let carpeta = std::env::args().nth(1).unwrap();
    let e = Entrada { comando: "/Applications/Narelia.app/Contents/MacOS/narelia-mcp".into(), args: vec![], carpeta };
    let mut out = vec![];
    for app in TODAS {
        let mut o = serde_json::json!({"nombre": app.nombre(), "a_mano": app.a_mano(), "grupo": format!("{:?}", app.grupo())});
        if let Some(f) = app.fichero_en(So::Mac, std::path::Path::new("~"), None) { o["fichero"] = f.to_string_lossy().into(); }
        for (k, i) in [("es", Idioma::Es), ("en", Idioma::En)] {
            if let Some(p) = clientes::a_mano(app, &e, So::Mac, i) { o[format!("texto")] = p.texto.into(); o[format!("donde_{k}")] = p.donde.into(); }
        }
        out.push(o);
    }
    println!("{}", serde_json::to_string_pretty(&out).unwrap());
}
