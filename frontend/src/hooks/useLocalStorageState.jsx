function useLocalStorageState(key, defaultValue) {
    // make a piece of state, and a function to update it,
    // like useState does
    const [state, setState] = useState(() => {
      let value;
      try {
        value = JSON.parse(
          window.localStorage.getItem(key) || String(defaultValue)
        );
      } catch (e) {
        value = defaultValue;
      }
      return value;
    });
  
    // use useEffect to update localStorage when state changes
    useEffect(() => {
      window.localStorage.setItem(key, JSON.stringify(state));
    }, [state]);
  
    return [state, setState];
  }