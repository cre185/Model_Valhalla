const serverAddress = '43.138.44.44:8000';

const apiCat = (api: string) => {
  return `http://${serverAddress}${api}`;
};

export default apiCat;
