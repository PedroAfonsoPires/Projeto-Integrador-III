int fatorial (int n) {

	int valor = 1;
	for (; n > 0; n--) {
		valor = valor * n;
	}
	return valor;
}

