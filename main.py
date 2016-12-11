import numpy as np
import parser

counter = np.arange(38)  # счетчик html-страниц
vparser = np.vectorize(parser.parse_page)
vparser(counter)
