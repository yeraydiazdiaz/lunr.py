const fs = require('fs')
const tmp = require('tmp')
const lunr = require('lunr')
require("lunr-languages/lunr.stemmer.support")(lunr)
require("lunr-languages/lunr.es")(lunr)

const data = JSON.parse(
  fs.readFileSync(__dirname + '/../fixtures/lang_es.json'))
let documents = {}
const idx = lunr(function () {
  this.use(lunr.es)
  this.field('title')
  this.field('text')
  this.ref('id')
  for (doc of data.docs) {
    this.add(doc)
    documents[doc.id] = doc
  }
})

const tmpFile = tmp.fileSync({keep: true})
fs.writeFileSync(tmpFile.fd, JSON.stringify(idx))
process.stdout.write(tmpFile.name)
