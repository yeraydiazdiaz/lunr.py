use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod stemmer;

#[pyfunction]
fn stem(word: &str) -> PyResult<String>{
    let s = stemmer::get(word);
    match s {
        Ok(stemmed) => Ok(stemmed),
        Err(_e) => Ok(word.to_string()),  // TODO: maybe raise?
    }
}

#[pymodule]
fn rust_stemmer(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(stem))?;

    Ok(())
}