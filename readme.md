# Moody Chart

The purpose of this is to be able to create a custom moody chart to print out on a PDF. See the PDF's for the results.
The reason why I did this was because I wanted a chart that stretched across an entire page.

Adjust the parameters at the beginning of `moody_chart.py` to your liking.

I used the Haaland equation to gather data for the relative roughness lines. Historically, the Colebrook equation (a
more complex implicit relationship) is used to calculate the desired property; however, plotting the Colebrook equation
on top of the Haaland equation on a graph would be nearly indistinguishable.

See the latex branch for a better looking pdf with roughness values of common pipe materials.
