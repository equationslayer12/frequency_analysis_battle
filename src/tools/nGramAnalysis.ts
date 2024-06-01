import { game } from '@/game/Game';
import { ref, Ref } from 'vue';

/**
 * N-Gram analysis tool.
 * N-Gram: A sequence of n adjacent symbols.
 * For example, with an N size of 3, the Ngrams of the word FREQUENCY would be:
 * [FRE, REQ, EQU, QUE, UEN, ENC, NCY]
 * with N size of 6:
 * [FREQUE, REQUEN, EQUENC, QUENCY]
 */
export default class nGramAnalysis {
     /**
      * The size of the N-grams.
      */
     Nsize: Ref<number>;

     /**
      * The maximum number of letters per page.
      */
     maxLettersPerPage: Ref<number>;

     /**
      * The maximum number of N-grams per current page.
      */
     maxNgramPerCurrentPage: Ref<number>;

     /**
      * The number of N-grams per page.
      */
     nGramsPerPage: Ref<number>;

     /**
      * The maximum page number.
      */
     maxPage: Ref<number>;

     /**
      * The current page number.
      */
     currentPage: Ref<number>;

     /**
      * Count of each N-gram.
      */
     NgramsCount: Ref<{ [key: string]: number }>;

     /**
      * Array containing the most frequent N-grams.
      */
     mostFrequentNgrams: Ref<string[]>;

     /**
      * Constructs an instance of the N-Gram analysis tool.
      * @param Nsize The size of the N-grams.
      */
     constructor(Nsize: number) {
          this.Nsize = ref(Nsize);
          this.maxLettersPerPage = ref(40);
          this.nGramsPerPage = ref(
               Math.min(Math.floor(this.maxLettersPerPage.value / Nsize), 12)
          );
          this.currentPage = ref(0);
          this.maxNgramPerCurrentPage = ref(1);

          this.NgramsCount = ref({});
          this.mostFrequentNgrams = ref([]);
          this._countNgrams();
          this._updateMaxNgramPerCurrentPage();

          let totalNgrams = Object.keys(this.NgramsCount.value).length;
          this.maxPage = ref(Math.ceil(totalNgrams / this.nGramsPerPage.value));
     }

     /**
      * Count the N-Grams in the words array, and update NgramsCount and mostFrequentNgrams accordingly.
      */
     private _countNgrams(): void {
          for (let nGram in this.NgramsCount.value)
               delete this.NgramsCount.value[nGram];

          this.NgramsCount.value = {};
          for (let i = 0; i < game.wordsArray.length; i++) {
               const word = game.wordsArray[i];
               for (let j = 0; j < word.length - this.Nsize.value + 1; j++) {
                    const nGram = word.slice(j, j + this.Nsize.value);
                    if (this.NgramsCount.value[nGram])
                         this.NgramsCount.value[nGram]++;
                    else this.NgramsCount.value[nGram] = 1;
               }
          }

          var mostFrequentNgrams = Object.keys(this.NgramsCount.value);
          mostFrequentNgrams.sort(
               (a, b) => this.NgramsCount.value[b] - this.NgramsCount.value[a]
          );
          this.mostFrequentNgrams.value = mostFrequentNgrams;
     }

     /**
      * Changes the size of the N-grams.
      * @param value The value by which to change the N size.
      */
     public changeNSize(value: number): void {
          this.Nsize.value += value;
          this.nGramsPerPage.value = Math.min(
               Math.floor(this.maxLettersPerPage.value / this.Nsize.value),
               12
          );

          this.currentPage.value = 0;
          this._countNgrams();
          this._updateMaxNgramPerCurrentPage();
     }

     /**
      * Changes the current page of N-grams.
      * @param count The number of pages to change.
      */
     public changeNgramPage(count: number): void {
          this.currentPage.value += count;
          if (this.currentPage.value < 0) {
               this.currentPage.value = this.maxPage.value - 1;
          } else if (this.maxPage.value <= this.currentPage.value) {
               this.currentPage.value %= this.maxPage.value;
          }

          this._updateMaxNgramPerCurrentPage();
     }

     /**
      * Updates the maximum number of N-grams per current page.
      */
     private _updateMaxNgramPerCurrentPage(): void {
          this.maxNgramPerCurrentPage.value = 0;
          const pageStartIndex =
               this.currentPage.value * this.nGramsPerPage.value;
          const pageEndIndex = Math.min(
               this.mostFrequentNgrams.value.length,
               pageStartIndex + this.nGramsPerPage.value
          );
          for (let i = pageStartIndex; i < pageEndIndex; i++) {
               const nGram = this.mostFrequentNgrams.value[i];
               this.maxNgramPerCurrentPage.value = Math.max(
                    this.NgramsCount.value[nGram],
                    this.maxNgramPerCurrentPage.value
               );
          }
     }
}
