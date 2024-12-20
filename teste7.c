    void quicksort (int ini, int fim, int *vetor) {
    if (ini < fim) {
    int meio = (ini+fim)/2;
    int pivot = vetor[meio];

    int ee = ini;
    int ff = fim;

    while (ee < ff) {
    while (ee <= fim && vetor[ee]<pivot){ ee=ee+1;}
    while (ff >= ini && vetor[ff]>pivot){ ff=ff-1;}
    if (ee<=ff) {
    int aux = vetor[ee];
    vetor[ee]= vetor[ff];
    vetor[ff]=aux;
    ee = ee+1;
    ff = ff - 1;
    }
    }
    quicksort(ini,ff,vetor);
    quicksort(ee,fim,vetor);
    }
    }
