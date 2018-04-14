const documents = [
  {
    "id": "a",
    "text": "Este es un ejemplo inventado de lo que sería un documento en el idioma que se más se habla en España.",
    "title": "Ejemplo de documento en español"
  },
  {
    "id": "b",
    "text": "Según un estudio que me acabo de inventar porque soy un experto en idiomas que se hablan en España.",
    "title": "Español es el tercer idioma más hablado del mundo"
  },
]


const lunr = require("lunr")
require("lunr-languages/lunr.stemmer.support")(lunr)
require("lunr-languages/lunr.es")(lunr)

let docsByRef = {};
let idx = lunr(function () {
  this.use(lunr.es);
  this.ref('id');
  this.field('title');
  this.field('text');

  documents.forEach(doc => {
    this.add(doc);
    docsByRef[doc.id] = doc;
  });
});

function search(query) {
  console.log(`Searching for "${query}"`);
  let results = idx.search(query);
  for (result of results) {
    process.stdout.write(`${result.ref} "${docsByRef[result.ref].title}" [${result.score}]\n`)
  }
}

let queries = ['inventar', 'documento', 'españa'];
queries.forEach(q => search(q));
