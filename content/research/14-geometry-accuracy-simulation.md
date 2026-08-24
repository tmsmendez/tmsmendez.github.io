---
title: Geometry accuracy in acoustic simulation
description: How NURBS and mesh representations change the results of room acoustic ray tracing.
img: assets/img/nubrsvmesh.png
importance: 14
category: Politecnico di Torino
gallery:
  - [nubrsvmesh.png]
---

Room acoustic ray tracing is usually run on triangulated meshes, because intersecting a ray with a triangle is cheap. But a curved reflector approximated by facets is not the reflector that was designed: each facet sends its rays off in a slightly wrong direction, and the errors accumulate over successive reflections. For halls whose acoustics depend on doubly curved surfaces — exactly the geometries that form-finding produces — this turns a modelling convention into a source of error in the result.

This research compared ray tracing performed directly on NURBS geometry against the same surfaces tessellated at varying resolutions, tracking how mesh density shifts the computed acoustic parameters and how fine a tessellation has to be before the difference disappears. The results give a practical rule for when the extra cost of exact geometry is worth paying, and when it is not.

#### Collaborators

- [Arianna Astolfi — Politecnico di Torino](https://www.polito.it/personale?p=arianna.astolfi)
- [Mario Sassone — Politecnico di Torino](https://www.polito.it/personale?p=mario.sassone)
- [Louena Shtrepi — Politecnico di Torino](https://www.polito.it/personale?p=louena.shtrepi)
- [Arthur van der Harten — Pachyderm Acoustic](https://www.pachydermacoustic.com/)
- Elena Badino — Politecnico di Torino

#### Publications

- [NURBS and mesh geometry in room acoustic ray-tracing simulation (AIA-DAGA 2013)](/publications/)
- [Investigating the importance of geometrical accuracy in acoustic simulations: A comparison of NURBS and mesh-based approaches (ISRA 2019)](/publications/)
