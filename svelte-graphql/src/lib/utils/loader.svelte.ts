// loader.svelte.ts

export type LoaderType = {
  isLoading: boolean;      
  readonly showSlowMessage: boolean;
};

export function createLoader() {
  let _isLoading = $state(false);
  let _showSlowMessage = $state(false);
  let timerId: ReturnType<typeof setTimeout> | null = null;

  return {
    
    get isLoading() {
      return _isLoading;
    },

    
    set isLoading(value: boolean) {
      _isLoading = value;

      if (timerId) {
          clearTimeout(timerId);
          timerId = null;
      }

      if (value) {
          
          timerId = setTimeout(() => {
              _showSlowMessage = true;
          }, 1000);
      } else {
          _showSlowMessage = false;
      }
    },

    get showSlowMessage() {
      return _showSlowMessage;
    }
  };
}