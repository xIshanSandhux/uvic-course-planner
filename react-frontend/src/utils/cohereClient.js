// src/utils/cohereClient.js
import { CohereClientV2 } from "cohere-ai";

export const client = new CohereClientV2({
  token: import.meta.env.VITE_COHERE_API_KEY,
});
