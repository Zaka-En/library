import type { MyReadingProgress$result } from "$houdini"
import type { ReadingProgressType, BookType } from "../app";
import { HTMLAttributes } from 'svelte/elements';
// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		
	}

	type ReadingProgressType = NonNullable<MyReadingProgress$result['myReadingProgress']>[number]
	type BookType = NonNullable<ReadingProgressType['book']>
	type CategoryType = {
    name: string;
    description: string;
    totalBooks: number;
  }

	namespace svelteHTML{
		interface HTMLAttributes<T> {
      // all elements can have an onenterviewport attribute
      'onenterviewport'?: () => void;
    }
	}
  
}

export {
	BookType,
	ReadingProgressType
};
