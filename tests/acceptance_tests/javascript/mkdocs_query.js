const fs = require('fs')
const lunr = require('lunr')

const data = JSON.parse(
  fs.readFileSync(__dirname + '/../fixtures/mkdocs_index.json'))
let documents = {}
const idx = lunr(function () {
  this.field('title')
  this.field('text')
  this.ref('id')
  for (doc of data.docs) {
    this.add(doc)
    documents[doc.id] = doc
  }
})

let results = idx.search(process.argv[2])
for (result of results) {
  let doc = documents[result.ref]
  process.stdout.write(`${result.ref} "${doc.title}" [${result.score}]\n`)
}
