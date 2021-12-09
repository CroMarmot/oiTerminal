#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
#define t3 1000+10
#define t4 10000+10
#define t5 100000+10
#define t6 1000000+10
#define MOD 1000000007
#define rep(i,a,n) for (ll i=a;i<n;i++)
#define per(i,a,n) for (ll i=n-1;i>=a;i--)
#define pb push_back
const double pi = acos(-1.0);

namespace X{
  ll r(){ll r;scanf("%lld",&r);return r;} // read
  void add(ll &v0,ll &v1){(v0+=v1%MOD)%=MOD;} // add with MOD
  ll mpow(ll v,ll mi){ll r = 1;while(mi){if(mi%2)(r*=v)%=MOD;(v*=v)%=MOD;mi>>=1;};return r;} // quick power with MOD
  ll mod(ll v){return (v%MOD+MOD)%MOD;} // output
  ll gcd(ll a,ll b){return b == 0?a:gcd(b,a%b);}
};

int main(){
  return 0;
}

/*
 *
 * hash prime
   61,83,113,151,211,281,379,509683,911
   1217,1627,2179,2909,3881,6907,9209
   12281,16381,21841,29123,38833,51787,69061,92083
   122777,163729,218357,291143,388211,517619,690163,999983
   1226959,1635947,2181271,2908361,3877817,5170427,6893911,9191891
   12255871,16341163,21788233,29050993,38734667,51646229,68861641,91815541
   122420729,163227661,217636919,290182597,386910137,515880193,687840301,917120411
   1000000007,1000000009
 * */
