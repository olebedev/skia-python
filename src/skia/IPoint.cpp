#include <pybind11/pybind11.h>
#include <skia.h>

namespace py = pybind11;

void IPoint(py::module &m) {
py::class_<SkIPoint>(m, "IPoint");
}