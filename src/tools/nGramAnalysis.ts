import textUtil from '../tools/TextUtil'
import {ref, Ref} from 'vue'

/**
 * N-Gram analysis tool.
 * N-Gram: A sequence of n adjacent symbols.
 * For example, with an N size of 3, the Ngrams of the word FREQUENCY would be:
 * [FRE, REQ, EQU, QUE, UEN, ENC, NCY]
 * with N size of 6:
 * [FREQUE, REQUEN, EQUENC, QUENCY]
 */
export default class nGramAnalysis {
    Nsize: Ref
    maxLettersPerPage: Ref
    maxNgramPerCurrentPage: Ref
    nGramsPerPage: Ref
    maxPage: Ref
    currentPage: Ref
    NgramsCount: Ref
    mostFrequentNgrams: Ref

    constructor(Nsize: number) {
        this.Nsize = ref(Nsize);
        this.maxLettersPerPage = ref(40);
        this.nGramsPerPage = ref(
            Math.min(
                Math.floor(this.maxLettersPerPage.value / Nsize),
                12
            )
        );
        this.currentPage = ref(0);
        this.maxNgramPerCurrentPage = ref(1);

        this.NgramsCount = ref({});
        this.mostFrequentNgrams = ref([]);
        this._countNgrams();
        this._updateMaxNgramPerCurrentPage()
        
        let totalNgrams = Object.keys(this.NgramsCount.value).length
        this.maxPage = ref(Math.ceil(totalNgrams / this.nGramsPerPage.value));
        console.log(this.maxPage.value);
    }

    /**
     * count the N-Grams in the words array, and update NgramsCount and mostFrequentNgrams accordingly.
     */
    _countNgrams() {
        for (var nGram in this.NgramsCount.value)
            delete this.NgramsCount.value[nGram];

        this.NgramsCount.value = {};
        for (let i = 0; i < textUtil.wordsArray.length; i++) {
            const word = textUtil.wordsArray[i];
            for (let j = 0; j < word.length - this.Nsize.value + 1; j++) {
                const nGram = word.slice(j, j + this.Nsize.value);
                if (this.NgramsCount.value[nGram])
                    this.NgramsCount.value[nGram] ++;
                else
                    this.NgramsCount.value[nGram] = 1;
                
            }
        }
        
        var mostFrequentNgrams = Object.keys(this.NgramsCount.value)
        mostFrequentNgrams.sort((a, b) => this.NgramsCount.value[b] - this.NgramsCount.value[a]);
        this.mostFrequentNgrams.value = mostFrequentNgrams;
    }

    changeNSize(value: number) {
        this.Nsize.value += value;
        this.nGramsPerPage.value = Math.min(
            Math.floor(this.maxLettersPerPage.value / this.Nsize.value),
            12
        );

        this.currentPage.value = 0;
        this._countNgrams()
        this._updateMaxNgramPerCurrentPage()
    }

    changeNgramPage(count: number) {
        this.currentPage.value += count;
        if (this.currentPage.value < 0) {
            this.currentPage.value = this.maxPage.value - 1;
        }
        else if (this.maxPage.value <= this.currentPage.value) {
            this.currentPage.value %= this.maxPage.value;
        }

        this._updateMaxNgramPerCurrentPage();
    }

    _updateMaxNgramPerCurrentPage() {
        this.maxNgramPerCurrentPage.value = 0;
        const pageStartIndex = this.currentPage.value * this.nGramsPerPage.value
        const pageEndIndex = Math.min(this.mostFrequentNgrams.value.length, pageStartIndex + this.nGramsPerPage.value);
        for (let i = pageStartIndex; i < pageEndIndex; i++) {
            const nGram = this.mostFrequentNgrams.value[i];
            this.maxNgramPerCurrentPage.value = Math.max(this.NgramsCount.value[nGram], this.maxNgramPerCurrentPage.value);
        }
    }
}


// var NgramsCount = ref({});



// function updateNgramPage(count) {
//     currentNgramPage.value += count;
//     if (currentNgramPage.value < 0) {
//         currentNgramPage.value = maxNgramPage - 1;
//     }
//     else if (maxNgramPage <= currentNgramPage.value) {
//         currentNgramPage.value %= maxNgramPage;
//     }
//     maxNgramCountForPage = findMaxNgramCountForPage();
//     console.log(maxNgramCountForPage);
// }

// var maxNgramCountForPage = findMaxNgramCountForPage();
// function findMaxNgramCountForPage() {
    
//     var maxNgramCount = 0;
//     console.log(maxNgramCount);
//     for (let i = currentNgramPage.value*nGramsPerPage; i < currentNgramPage.value*nGramsPerPage + nGramsPerPage; i++) {
//         console.log(` current index: ${i}`);
//         const nGram = mostFrequentNgrams[i];
//         console.log(` current nGram: ${nGram}`);
//         maxNgramCount = Math.max(NgramsCount.value[nGram], maxNgramCount);
//     }
//     console.log(maxNgramCount);
//     return maxNgramCount;
// }
