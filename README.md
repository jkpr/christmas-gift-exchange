# Make Christmas Merry Again

Generate Christmas gift assignments for a family.

Requires input data in JSON format. Required keys are:

- `people`: a list of strings for the names. The names should be unique
- `spouses`: a list of lists. Each inner list has the names of a single couple.
- `last_year`: a map of who gave to whom last year. An empty list is ok.

See the [input data template](input_template.json).

## Rules

1. Do not repeat last year's assignments
2. Do not assign someone to himself/herself or his/her spouse
3. Two spouses should not give to two other spouses
4. The santa list should be a [cyclic permutation](https://en.wikipedia.org/wiki/Cyclic_permutation).