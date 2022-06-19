from scipy import stats


def przewidywanie_spalanie(moc, spalanie, moc_klient):
   slope, intercept, r, p, std_err = stats.linregress(moc, spalanie)
   return slope * moc_klient + intercept

