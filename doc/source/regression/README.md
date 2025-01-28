# Regression folder

This folder contains various useful examples illustrating how to use and how not
to use PyWavelets.

The examples are written in the [MyST markdown notebook
format](https://myst-nb.readthedocs.io/en/v0.13.2/use/markdown.html). This
allows each .md file to function simultaneously as documentation that can be fed
into Sphinx and as a source file that can be converted to the Jupyter notebook
format (.ipynb), which can then be opened in notebook applications such as
JupyterLab. For this reason, each example page in this folder includes a header template
that adds a blurb to the top of each page about how the page can be
run or downloaded as a Jupyter notebook.

There are a few shortcomings to this approach of generating the code cell outputs in
the documentation pages at build time rather than hand editing them into the
document source file. One is that we can no longer compare the generated outputs
with the expected outputs as we used to do with doctest. Another is that we
lose some control over how we want the outputs to appear, unless we use a workaround.

Here is the workaround we created. First we tell MyST-NB to remove the generated
cell output from the documentation page by adding the `remove-output` tag to the
`code-cell` directive in the markdown file. Then we hand code the output in a
`code-block` directive, not to be confused with `code-cell`! The `code-cell`
directive says "I am notebook code cell input, run me!" The `code-block`
directive says, "I am just a block of code for documentation purposes, don't run
me!" To the code block, we add the `.pywt-handcoded-cell-output` class so that
we can style it to look the same as other cell outputs on the same HTML page.
Finally, we tag the handcoded output with `jupyterlite_sphinx_strip` so that we
can exclude it when converting from .md to .ipynb. That way only generated
output appears in the .ipynb notebook.

To recap:

- We use the `remove-output` tag to remove the **generated** code cell output
  during .md to .html conversion (this conversion is done by MyST-NB).
- We use the `jupyterlite_sphinx_strip` tag to remove the **handcoded** output
  during .md to .ipynb conversion (this conversion is done by Jupytext).

Example markdown:

    ```{code-cell}
    :tags: [raises-exception, remove-output]
    1 / 0
    ```

    +++ {"tags" ["jupyterlite_sphinx_strip"]}

    ```{code-block} python
    :class: pywt-handcoded-cell-output
    Traceback (most recent call last):
    ...
    ZeroDivisionError: division by zero
    ```
