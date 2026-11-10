#include <stdio.h>

#include <auth/auth.h>
#include <auth/permissions.h>
#include <auth/token.h>

// prints every enum value of libauth as "NAME VALUE", from the maps of its headers,
// so unit/test_constants.py compares the constants of the package with the real ones

int main (void) {

	#define XX(num, name, string) (void) printf ("PERCEPTHOR_AUTH_TYPE_%s %d\n", #name, num);
	PERCEPTHOR_AUTH_TYPE_MAP(XX)
	#undef XX

	#define XX(num, name, string) (void) printf ("PERCEPTHOR_AUTH_SCOPE_%s %d\n", #name, num);
	PERCEPTHOR_AUTH_SCOPE_MAP(XX)
	#undef XX

	#define XX(num, name, string) (void) printf ("PERMISSIONS_TYPE_%s %d\n", #name, num);
	PERMISSIONS_TYPE_MAP(XX)
	#undef XX

	#define XX(num, name, string) (void) printf ("PERCEPTHOR_TOKEN_TYPE_%s %d\n", #name, num);
	PERCEPTHOR_TOKEN_TYPE_MAP(XX)
	#undef XX

	return 0;

}
