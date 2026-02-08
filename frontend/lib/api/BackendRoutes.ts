/**
 * MESA (Medical Expert System Assistant) API Routes
 * All routes are relative - ApiClient handles the base URL
 */

export const MesaRoutes = {
  /* -------- General -------- */
  root: `/`,
  ping: `/ping`,

  /* -------- Expert System -------- */
  diagnose: `/expert/diagnose`,
  symptoms: `/expert/symptoms`,
  diseases: `/expert/diseases`,
  disease: (name: string) => `/expert/diseases/${name}`,

  /* -------- AI Chat -------- */
  chatMessage: `/chat/message`,
  chatModels: `/chat/models`,
  validateModel: `/chat/validate-model`,
};
