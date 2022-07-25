# dbignite
__Health Data Interoperability__

This library is designed to provide a low friction entry to performing analytics on 
[FHIR](https://hl7.org/fhir/bundle.html) bunldes, by extracting patient resources and
writing the data in deltalake. 

# Usage Examples
In this first phase of development, we drive
towards the following core use case. At the same
time we ensure the spec. is [extensible for the future
use cases](#future-extensions).

## Core Use Case: Quick Exploratory Analysis of a FHIR Bundle

The _data_model_ module contains a suite of common
health data models such as FHIR, or OMOP CDM. 

See: [DataModels](#datamodels)

### Example usecase:

```
from dbignite.data_model import Transformer
transformer=Transformer(spark)
cdm=transformer.fhir_bundles_to_omop_cdm(BUNDLE_PATH, cdm_database='dbignite_demo')
```

The returned value of the `cdm` is an OmopCDM object with an associated database (`dbignite_demo`), containing the following tables:

- condition
- encounter
- person
- procedure_occurrence

Which are automaically created and added to the specified database (`'dbignite_demo'` in the example above.
As a usecase, one can simply construct cohorts based on these tables and add the cohorts to the same schema or a new schema.

For example you can write `select * from dbignite_demo.person where year_of_birth > 1982 and gender_source_value='male'` to select all male patients who are under 40. 

> [See this in a notebook.](demo.py)

# Interop Pipeline Design

## DataModels
_DataModels_ hold the state of an interoperable _DataModel_ 
such as FHIR bundles, or OMOP CDM. the _Transformer_ class contains 
pre-defined transformations from one data model to another one.

[![](https://mermaid.ink/img/eyJjb2RlIjoiY2xhc3NEaWFncmFtXG4gICAgRGF0YU1vZGVsIDx8LS0gUGVyc29uRGFzaGJvYXJkXG4gICAgRGF0YU1vZGVsIDx8LS0gT21vcENkbVxuICAgIERhdGFNb2RlbCA8fC0tIEZoaXJCdW5kbGVzXG4gICAgRGF0YU1vZGVsOiArYnVpbGRlcihmcm9tXyBEYXRhTW9kZWwpJFxuICAgIERhdGFNb2RlbDogK3N1bW1hcnkoKSBEYXRhRnJhbWVcbiAgICBEYXRhTW9kZWw6ICtsaXN0RGF0YWJhc2VzKCkgTGlzdH5EYXRhYmFzZX5cblxuICAgIFxuICAgICIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/edit/#eyJjb2RlIjoiY2xhc3NEaWFncmFtXG4gICAgRGF0YU1vZGVsIDx8LS0gUGVyc29uRGFzaGJvYXJkXG4gICAgRGF0YU1vZGVsIDx8LS0gT21vcENkbVxuICAgIERhdGFNb2RlbCA8fC0tIEZoaXJCdW5kbGVzXG4gICAgRGF0YU1vZGVsOiArYnVpbGRlcihmcm9tXyBEYXRhTW9kZWwpJFxuICAgIERhdGFNb2RlbDogK3N1bW1hcnkoKSBEYXRhRnJhbWVcbiAgICBEYXRhTW9kZWw6ICtsaXN0RGF0YWJhc2VzKCkgTGlzdH5EYXRhYmFzZX5cblxuICAgIFxuICAgICIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkZWZhdWx0XCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)


## Transformers
One of the key challenges for interoperability of data models is a
"many to many" problem. Support for any new data model requires
cross compatability with many other data models. Intermediate
data models can mitigate this issue.

### The "Many to Many" Problem
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW0FdIC0tPnx0cmFuc2Zvcm18IEIoQilcbiAgICBBW0FdIC0tPnx0cmFuc2Zvcm18IEMoQylcbiAgICBCW0JdIC0tPnx0cmFuc2Zvcm18IEEoQSlcbiAgICBCW0JdIC0tPnx0cmFuc2Zvcm18IEMoQylcbiAgICBDW0NdIC0tPnx0cmFuc2Zvcm18IEEoQSlcbiAgICBDW0NdIC0tPnx0cmFuc2Zvcm18IEIoQilcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBBW0FdIC0tPnx0cmFuc2Zvcm18IEIoQilcbiAgICBBW0FdIC0tPnx0cmFuc2Zvcm18IEMoQylcbiAgICBCW0JdIC0tPnx0cmFuc2Zvcm18IEEoQSlcbiAgICBCW0JdIC0tPnx0cmFuc2Zvcm18IEMoQylcbiAgICBDW0NdIC0tPnx0cmFuc2Zvcm18IEEoQSlcbiAgICBDW0NdIC0tPnx0cmFuc2Zvcm18IEIoQilcbiIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkZWZhdWx0XCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

Pipelining existing transforms can significantly simplify
the problem of mapping a variety of data models.
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBYW0FdIC0tLXx0cmFuc2Zvcm18IEkoSW50ZXJtZWRpYXRlIERhdGFNb2RlbCBYKVxuICAgIFlbQl0gLS0tfHRyYW5zZm9ybXwgSShJbnRlcm1lZGlhdGUgRGF0YU1vZGVsIFgpXG4gICAgWltDXSAtLS18dHJhbnNmb3JtfCBJKEludGVybWVkaWF0ZSBEYXRhTW9kZWwgWClcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiZ3JhcGggTFJcbiAgICBYW0FdIC0tLXx0cmFuc2Zvcm18IEkoSW50ZXJtZWRpYXRlIERhdGFNb2RlbCBYKVxuICAgIFlbQl0gLS0tfHRyYW5zZm9ybXwgSShJbnRlcm1lZGlhdGUgRGF0YU1vZGVsIFgpXG4gICAgWltDXSAtLS18dHJhbnNmb3JtfCBJKEludGVybWVkaWF0ZSBEYXRhTW9kZWwgWClcbiIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkZWZhdWx0XCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)

### Making Pipelines with Simple Composition
Using methods in _Transformers_ we can transform one datamodel to another.
This pattern also allows simple combination of transformations.

[![](https://mermaid.ink/img/eyJjb2RlIjoiY2xhc3NEaWFncmFtXG4gICAgZmhpcl9idW5kbGVzX3RvX3BlcnNvbl9kYXNoYm9hcmQgLi4-IGZoaXJfYnVuZGxlc190b19vbW9wX2NkbSA6ICgxKSBjYWxsc1xuICAgIGZoaXJfYnVuZGxlc190b19wZXJzb25fZGFzaGJvYXJkIC4uPiBvbW9wX2NkbV90b19wZXJzb25fZGFzaGJvYXJkIDogKDIpIGNhbGxzXG4gICAgZmhpcl9idW5kbGVzX3RvX3BlcnNvbl9kYXNoYm9hcmQ6ICtfX2NhbGxfXyhTdHJpbmcgYnVuZGxlX3BhdGgpKiBQZXJzb25EYXNoYm9hcmRcbiAgICBmaGlyX2J1bmRsZXNfdG9fb21vcF9jZG06ICtfX2NhbGxfXyhTdHJpbmcgYnVuZGxlX3BhdGgpKiBPbW9wQ2RtXG4gICAgb21vcF9jZG1fdG9fcGVyc29uX2Rhc2hib2FyZDogK19fY2FsbF9fKFN0cmluZyBkYXRhYmFzZSkqIFBlcnNvbkRhc2hib2FyZFxuICAgIFxuICAgICIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2UsImF1dG9TeW5jIjp0cnVlLCJ1cGRhdGVEaWFncmFtIjpmYWxzZX0)](https://mermaid.live/edit#eyJjb2RlIjoiY2xhc3NEaWFncmFtXG4gICAgZmhpcl9idW5kbGVzX3RvX3BlcnNvbl9kYXNoYm9hcmQgLi4-IGZoaXJfYnVuZGxlc190b19vbW9wX2NkbSA6ICgxKSBjYWxsc1xuICAgIGZoaXJfYnVuZGxlc190b19wZXJzb25fZGFzaGJvYXJkIC4uPiBvbW9wX2NkbV90b19wZXJzb25fZGFzaGJvYXJkIDogKDIpIGNhbGxzXG4gICAgZmhpcl9idW5kbGVzX3RvX3BlcnNvbl9kYXNoYm9hcmQ6ICtfX2NhbGxfXyhTdHJpbmcgYnVuZGxlX3BhdGgpKiBQZXJzb25EYXNoYm9hcmRcbiAgICBmaGlyX2J1bmRsZXNfdG9fb21vcF9jZG06ICtfX2NhbGxfXyhTdHJpbmcgYnVuZGxlX3BhdGgpKiBPbW9wQ2RtXG4gICAgb21vcF9jZG1fdG9fcGVyc29uX2Rhc2hib2FyZDogK19fY2FsbF9fKFN0cmluZyBkYXRhYmFzZSkqIFBlcnNvbkRhc2hib2FyZFxuICAgIFxuICAgICIsIm1lcm1haWQiOiJ7XG4gIFwidGhlbWVcIjogXCJkZWZhdWx0XCJcbn0iLCJ1cGRhdGVFZGl0b3IiOmZhbHNlLCJhdXRvU3luYyI6dHJ1ZSwidXBkYXRlRGlhZ3JhbSI6ZmFsc2V9)
