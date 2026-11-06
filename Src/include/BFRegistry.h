// BFRegistry.h - self-registration of manager and UI classes.
// Every translation unit that includes a class header gets one static registrar for it; its dynamic
// initializer builds a temporary std::string from the class name and registers T::create once
// (guarded by T::s_registered). 887 copies in zoo.exe (cluster "182-byte static initialisers").
// The post-link optimizer inlined _STL_alloc_proxy's constructor in the originals (sub esp,4 ...
// add esp,0xc); compare.py accounts for that.
#ifndef BFREGISTRY_H
#define BFREGISTRY_H
#include <string>

class BFMgr;
class UIElement;
typedef BFMgr* (*BFMgrCreateFn)();
typedef UIElement* (*UICreateFn)();

struct BFMgrFactory {
    static bool registerMgr(const std::string& name, BFMgrCreateFn create);       // 0x5770E5
};
struct UIFactory {
    static bool registerElement(const std::string& name, UICreateFn create);      // 0x5774BF
};

template<class T> struct BFMgrRegistrar {
    BFMgrRegistrar(const std::string& name) {
        if (!T::s_registered) { BFMgrFactory::registerMgr(name, T::create); T::s_registered = true; }
    }
};
template<class T> struct UIRegistrar {
    UIRegistrar(const std::string& name) {
        if (!T::s_registered) { UIFactory::registerElement(name, T::create); T::s_registered = true; }
    }
};

#define BF_REGISTER_MGR(cls) static BFMgrRegistrar<cls> s_##cls##Registrar(cls::s_className)
#define UI_REGISTER(cls)     static UIRegistrar<cls> s_##cls##Registrar(cls::s_className)

#endif
