# Moody Chart

The purpose of this is to be able to create a custom moody chart to print out on a PDF. See the PDF's for the results.
The reason why I did this was because I wanted a chart that stretched across an entire page.

Adjust the parameters at the beginning of `moody_chart.py` to your liking.

There is no use of numerical solvers unlike some other moody charts I've seen. Instead, I used the Haaland equation to
gather data for the relative roughness lines. Historically, the Colebrook equation (a more complex implicit
relationship) is used to calculate the desired property; however, plotting the Colebrook equation on top of the Haaland
equation on a graph would be nearly indistinguishable. In fact, I think I'll never use this chart ever because I could
just program my TI-84 to get a more precise solution.
