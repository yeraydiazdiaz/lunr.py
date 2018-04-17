const fs = require('fs')
const tmp = require('tmp')
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

const tmpFile = tmp.fileSync({keep: true})
fs.writeFileSync(tmpFile.fd, JSON.stringify(idx))
process.stdout.write(tmpFile.name)
