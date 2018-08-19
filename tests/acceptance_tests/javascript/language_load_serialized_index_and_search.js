const fs = require('fs')
const lunr = require('lunr')
require("lunr-languages/lunr.stemmer.support")(lunr)
require("lunr-languages/lunr.es")(lunr)

// Read the documents only to retrieve the title for the results
const fixtureName = process.argv[4] ||  'lang_es.json'
const fixturePath = __dirname + '/../fixtures/' + fixtureName
const data = JSON.parse(fs.readFileSync(fixturePath))
let documents = {}
for (doc of data.docs) {
  documents[doc.id] = doc
}

// Load the index from the serialized path produced from Python
const serializedIndex = JSON.parse(fs.readFileSync(process.argv[2]))
let idx = lunr.Index.load(serializedIndex)
let results = idx.search(process.argv[3])
for (result of results) {
  process.stdout.write(`${result.ref} "${documents[result.ref].title}" [${result.score}]\n`)
}