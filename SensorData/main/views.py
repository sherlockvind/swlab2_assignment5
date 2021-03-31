from django.shortcuts import render, get_object_or_404, redirect
from .utils import *

def home(request):
	#creating a random dataframe containing only values
	np.random.seed(1)
	rs = np.random.randn(100)
	xs = [[0, 0]]
	for idx, r in zip(range(1, len(rs) + 1), rs):
		q_val = xs[-1][1] * 0.9 + r
		xs.append([idx, q_val])

	df = pd.DataFrame(xs, columns=['time', 'quantity'])

	max_val = maximum(df)
	min_val = minimum(df)
	rel_max_count = count_relative_maxima(df)
	rel_min_count = count_relative_minima(df)
	(avg_dec_slope, avg_inc_slope) = calc_slopes(df, ('time', 'quantity'))

	context = {'max_val' : max_val, 'min_val' : min_val, 
			   'rel_max_count' : rel_max_count, 'rel_min_count' : rel_min_count, 'avg_inc_slope' : avg_inc_slope, 'avg_dec_slope' : avg_dec_slope}
	return render(request=request, template_name="main/home.html", context=context)