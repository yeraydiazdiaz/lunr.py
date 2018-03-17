const fs = require('fs')
const lunr = require('lunr')

// Read the documents only to retrieve the title for the results
const data = JSON.parse(
  fs.readFileSync(__dirname + '/fixtures/search_index.json'))
let documents = {}
for (doc of data.docs) {
  documents[doc.location] = doc
}

// Load the index from the serialized path produced from Python
const serializedIndex = JSON.parse(fs.readFileSync(process.argv[2]))
let idx = lunr.Index.load(serializedIndex)
let results = idx.search('plugins')
for (result of results) {
  process.stdout.write(`${result.ref} "${documents[result.ref].title}" [${result.score}]\n`)
}