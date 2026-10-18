// Excerpt from src/auth/roleAccess.ts
// Repository: Team-Sellora/sellora-web (develop branch). Shared for illustration only.

import type { SelloraRole } from "./useSelloraAuth";

export const routeAccess: Record<string, SelloraRole[]> = {
  "/provinces": ["CompanyAdmin"],
  "/area-managers": ["CompanyAdmin"],
  "/hierarchy-roll-up": ["CompanyAdmin"],
  // The API currently authorizes both agency and territory registration/listing
  // for Area Managers only; match that rule in the route guard.
  "/agencies": ["AreaManager"],
  "/territories": ["AreaManager"],
  "/territory-assignments": ["AreaManager"],
  "/sales-reps": ["AgencyOperator"],
  // POST /api/staff: Company Admins add any staff role, Agency Operators add Sales Reps.
  "/staff": ["CompanyAdmin", "AgencyOperator"],
  "/shops": ["AgencyOperator"],
  "/products": ["CompanyAdmin", "AreaManager", "AgencyOperator", "SalesRep"],
  "/products/new": ["CompanyAdmin"],
  // Categories are created and edited here (POST/PUT /api/categories are
  // RequireCompanyAdmin); everyone else sees categories on the Products page.
  "/product-categories": ["CompanyAdmin"],
  "/inventory": ["CompanyAdmin", "AgencyOperator", "SalesRep"],
  // Shop Owners can read their own shop's orders (server-side scoping).
  "/orders": ["CompanyAdmin", "AreaManager", "AgencyOperator", "SalesRep", "ShopOwner"],
  // POST /api/orders is RequireSalesRep on the server.
  "/orders/new": ["SalesRep"],
  // US-E4-6: reps see their own returns, operators their agency's, admins all.
  "/van-returns": ["CompanyAdmin", "AgencyOperator", "SalesRep"],
  // POST /api/van-returns is RequireSalesRep on the server.
  "/van-returns/new": ["SalesRep"],
  "/deliveries": ["CompanyAdmin", "AreaManager", "AgencyOperator", "SalesRep", "ShopOwner"],
  "/returns": ["CompanyAdmin", "AreaManager", "AgencyOperator", "SalesRep", "ShopOwner"],
  // US-E5-3: the Notification service's admin endpoints are RequireCompanyAdmin.
  "/notifications": ["CompanyAdmin"],
  // US-E7-1 / CSP-250: Immutable append-only audit log.
  "/audit": ["CompanyAdmin", "AreaManager"],
  // US-E7-2 / CSP-252: Aggregate sales reporting dashboard.
  "/reports": ["CompanyAdmin", "AreaManager"],
