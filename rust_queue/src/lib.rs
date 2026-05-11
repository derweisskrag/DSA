use pyo3::prelude::*;
use std::sync::Mutex; // Add this for thread safety

#[pyclass]
pub struct PriorityQueue {
    // Wrap the Vec in a Mutex so multiple threads can't corrupt it
    queue: Mutex<Vec<(i32, PyObject)>>, 
}

#[pymethods]
impl PriorityQueue {
    #[new]
    fn new() -> Self {
        PriorityQueue { queue: Mutex::new(Vec::new()) }
    }

    fn push(&self, py: Python, priority: i32, item: PyObject) {
        // ALLOW-THREADS: Releasing the GIL so other threads can run Python code
        // while Rust is busy sorting the Vec.
        py.allow_threads(move || {
            let mut data = self.queue.lock().unwrap();
            data.push((priority, item));
            data.sort_unstable_by(|a, b| b.0.cmp(&a.0));
        });
    }

    fn pop(&self, py: Python) -> Option<PyObject> {
        py.allow_threads(move || {
            let mut data = self.queue.lock().unwrap();
            data.pop().map(|(_prio, item)| item)
        })
    }
}

#[pymodule]
fn burmese_native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PriorityQueue>()?;
    Ok(())
}