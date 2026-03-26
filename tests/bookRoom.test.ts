import { test, expect } from "@playwright/test";

test.describe("Conference Room Booking", () => {
  // the user can successfully book a room
  // since then tests are running in parallel, I am gonna try to book the same room in two different browsers
  // one of them should fail
  // which one fails and which one succeeds => No one knows
  // However, the fact that at least one of them should fail
});
