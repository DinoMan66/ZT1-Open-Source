// uiscreenhandlers.cpp - small UI event handlers of zoo.exe: look a control up by id in the UI
// manager and show / hide / enable it. The handlers are named after their address (UIH_<address>)
// until the screens they belong to are identified.
#include "uicontrol.h"
#include "uimanager.h"
#include <list>
#include <set>
#include "ztentity.h"
#include "ztgame.h"
#include "uilistbox.h"
#include "uigraph.h"
#include "ztmapview.h"

// UIH_4017E5: the cached control with id 0x1B58 (name of the screen unknown)
extern ZTMapView* g_638068;

void f4ef75b(int a, int b);                        // 0x4EF75B
bool f4769ac();                                    // 0x4769AC

extern bool g_63813d;
extern char g_638f0b;
extern int g_63e44c;
extern bool g_639144;
extern bool g_639145;
extern bool g_639470;
extern unsigned int g_63ba40;
extern int g_63cd60;
extern unsigned int g_643670;
extern unsigned int g_643688;
extern int g_641b08, g_641b3c, g_6433d0, g_6433c8;
extern bool g_638856;
extern int g_63e46c;
extern bool g_63bbd0;
extern int g_63e450;
extern float g_639158, g_63e45c, g_63e454, g_63e458, g_63e468, g_63e464;
extern bool g_64e808;
extern unsigned int g_638f70, g_63e4a4;
extern bool g_638f74;
extern int g_654b14;
extern int g_64e660;
void f6162c0(int a);
void f48482b(int id);
_STL::string f4f00f6(int textId);                   // 0x4F00F6
_STL::string f41d39c(int a, int b, int c);          // 0x41D39C
void f61794a(int a);                               // 0x61794A
ZTEntity* f410f84();                               // 0x410F84: the selected entity of the current screen
extern char g_638680, g_6387a0, g_638700;
extern bool g_654b13, g_6390df;
extern unsigned int g_654b0c, g_63b9dc;
void f615d28(ZTEntity* entity);
void f615fd7(int a);
void f616006(int a);
void f516aef();
void f46a144(ZTEntity* entity);
extern bool g_64e6e8, g_63885c;
extern unsigned int g_64e6e0, g_643cd4;
extern char g_638710;
void f48c87d(ZTEntity* entity);
void f47108a(ZTEntity* entity);
extern _STL::list<ZTEntity*> g_639160;
extern char g_638660;
extern bool g_63ead4;
void f58b5ce(ZTEntity* entity);
void f4ef99b(int a);
void f4681b5();
extern bool g_63c86e, g_639531;
extern unsigned int g_63c870, g_63b9c0, g_654d18;
extern char g_638690;
void f488446(ZTEntity* entity);
void f4673b5(ZTEntity* entity);
void f617d66(ZTEntity* entity);
extern int g_6433c4;
void f50f396(int index);
extern _STL::list<ZTEntity*> g_639118, g_639474;
extern _STL::set<ZTEntity*> g_639460;
extern bool g_639120, g_63e334;
extern char g_638700;

void f40ee3d();
void f41d565();
void f58b67d();
void f468968();
void f4b2972();
void f4cb384(int a);
void f4da4fa();
void f443b60();
void f4e6bbd();
void f4e673b();
void f48d052();
void f45390c();
void f467c6f();
void f467e76(int a);
void f467fc8(int a);
void f5aeb82(int a);
void f5b108b();
void f5b14a4(int except);
void f53002b();
void f52fa39();
void f4f004a();
void f4f0979();
void f52feef(UIControl* control);
void f530a0e(UIControl* control);
void f530aff(UIControl* control);
void f530bf2(UIControl* control);
void UIH_52F686();

// 0x4017E5
ZTMapView* UIH_4017E5()
{
    if (!g_638068)
        g_638068 = static_cast<ZTMapView*>(g_uiManager.find(0x1b58));
    return g_638068;
}

// 0x476919
void UIH_476919()
{
    g_uiManager.find(0x25)->show();
}

// 0x516AD7
void UIH_516AD7()
{
    UIControl* control = g_uiManager.find(0x22b4);
    if (control)
        control->show();
}

// 0x4E0EE9: shows the parent of control 0x5974 (the argument is unused)
void UIH_4E0EE9(int unused)
{
    UIControl* control = g_uiManager.find(0x5974);
    if (control && control->m_unk74)
        control->m_unk74->show();
}

// 0x4E4C97
void UIH_4E4C97()
{
    UIControl* control = g_uiManager.find(0x5974);
    if (control)
        g_uiManager.f44316b(control);
}

// 0x4E2CDD
void UIH_4E2CDD()
{
    g_uiManager.find(0x3e8)->vslot21();
    UIH_4E0EE9(0);
}

// 0x4E40D9
void UIH_4E40D9()
{
    g_uiManager.find(0x3e9)->vslot21();
    UIH_4E0EE9(0);
}

// 0x443960: hides the control when it is flagged (bit 0)
void UIH_443960(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x4881C7
void UIH_4881C7()
{
    g_uiManager.find(0x15)->show();
    f4ef75b(0, 1);
}

// 0x6108F0: toggles the control with id 0x1E
void UIH_6108F0()
{
    UIControl* control = g_uiManager.find(0x1e);
    if (control)
    {
        if (control->m_flags & 1)
            control->hide();
        else
            control->show();
    }
}

// 0x4DA045
void UIH_4DA045(bool on)
{
    UIControl* control = g_uiManager.find(0x404);
    if (control)
    {
        if (on)
            control->enable();
        else
            control->disable();
    }
}

// 0x468FBA
void UIH_468FBA(int id, bool on)
{
    UIControl* control = g_uiManager.find(id);
    if (!control)
        return;
    if (on)
        control->enable();
    else
        control->disable();
}

// 0x4E66BF
void UIH_4E66BF()
{
    UIControl* control = g_uiManager.find(0xe1a);
    if (control)
        control->show();
    control = g_uiManager.find(0xe1c);
    if (control)
        control->show();
    control = g_uiManager.find(0xe24);
    if (control)
        control->show();
}

// 0x443AF8: shows the three controls 0xE, 0x323 and 0x29 except the one passed in
void UIH_443AF8(int except)
{
    UIControl* control;
    if (except != 0xe && (control = g_uiManager.find(0xe)) != 0)
        control->show();
    if (except != 0x323 && (control = g_uiManager.find(0x323)) != 0)
        control->show();
    if (except != 0x29 && (control = g_uiManager.find(0x29)) != 0)
        control->show();
}

// 0x5B1426
void UIH_5B1426(int except)
{
    UIControl* control;
    if (except != 0x10 && (control = g_uiManager.find(0x10)) != 0)
        control->show();
    if (except != 0xc && (control = g_uiManager.find(0xc)) != 0)
        control->show();
    if (except != 0x1f && (control = g_uiManager.find(0x1f)) != 0)
        control->show();
    if (except != 0x1e && (control = g_uiManager.find(0x1e)) != 0)
        control->show();
}

// 0x471831
void UIH_471831()
{
    UIControl* control = g_uiManager.find(0xded);
    if (control)
    {
        control->show();
        control->setFlag(0x10, true);
    }
    control = g_uiManager.find(0x25a);
    if (control)
        control->setFlag(0x10, true);
}

// 0x472348
void UIH_472348()
{
    UIControl* control = g_uiManager.find(0xded);
    if (control)
    {
        control->hide();
        control->setFlag(0x10, false);
    }
    control = g_uiManager.find(0x25a);
    if (control)
        control->setFlag(0x10, false);
}

// 0x4F9729
bool UIH_4F9729()
{
    bool found = false;
    UIControl* first = g_uiManager.find(0x1b);
    if (first && !(first->m_flags & 1))
        found = true;
    UIControl* second = g_uiManager.find(0x1c);
    if (second && !(second->m_flags & 1))
        return true;
    return found;
}

// 0x618C62
void UIH_618C62()
{
    UIControl* control = g_uiManager.find(0x803);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
}

// 0x477004
void UIH_477004()
{
    UIControl* control = g_uiManager.find(0x5de);
    if (control && control->flagBit(1))
        return;
    if (f4769ac())
    {
        UIControl* other = g_uiManager.find(5);
        if (other)
            other->show();
    }
}

// 0x477041
void UIH_477041()
{
    UIH_477004();
}

// 0x617EFB
void UIH_617EFB()
{
    g_uiManager.find(0x14)->show();
    f4ef75b(0, 1);
}

// 0x5198F4
void UIH_5198F4()
{
    UIControl* control = g_uiManager.find(6);
    if (control)
        control->show();
    control = g_uiManager.find(0xc65);
    if (control)
    {
        control->show();
        control->setFlag(0x10, true);
    }
    control = g_uiManager.find(0xc66);
    if (control)
    {
        control->show();
        control->setFlag(0x10, true);
    }
}

// 0x4E6B43
void UIH_4E6B43()
{
    UIControl* control = g_uiManager.find(0xe1a);
    if (control)
    {
        control->hide();
        control->vslot50(0xe1a, 0);
    }
    control = g_uiManager.find(0xe1c);
    if (control)
    {
        control->hide();
        control->vslot50(0xe1c, 0);
    }
    UIControl* other = g_uiManager.find(0xe24);
    if (other)
        other->hide();
}

// 0x4E4289
void UIH_4E4289()
{
    UIControl* control = g_uiManager.find(0xbc6);
    if (control)
        control->vslot50(0x7fb, 0);
    control = g_uiManager.find(0xbf1);
    if (control)
        control->vslot50(0x7fc, 0);
}

// 0x4DA59E: enables the two arrow controls 0xCEE / 0xCF2 depending on n (1..5)
void UIH_4DA59E(int n)
{
    UIControl* control = g_uiManager.find(0xcee);
    if (n >= 5)
        control->disable();
    else
        control->enable();
    control = g_uiManager.find(0xcf2);
    if (n <= 1)
        control->disable();
    else
        control->enable();
    f4da4fa();
}

// 0x5B135B
void UIH_5B135B(int except)
{
    UIControl* control;
    if (except != 8 && (control = g_uiManager.find(8)) != 0)
        control->show();
    if (except != 3 && (control = g_uiManager.find(3)) != 0)
        control->show();
    if (except != 4 && (control = g_uiManager.find(4)) != 0)
        control->show();
    if (except != 0xa && (control = g_uiManager.find(0xa)) != 0)
        control->show();
    if (except != 0xf && (control = g_uiManager.find(0xf)) != 0)
        control->show();
    if (except != 5 && (control = g_uiManager.find(5)) != 0)
        control->show();
    if (except != 0x22 && (control = g_uiManager.find(0x22)) != 0)
        control->show();
}

// 0x519C1B
void UIH_519C1B()
{
    f40ee3d();
    f41d565();
    f58b67d();
    UIControl* control = g_uiManager.find(0x430);
    if (control)
    {
        control->show();
        control->setFlag(0x10, true);
    }
    control = g_uiManager.find(0x42f);
    if (control)
        control->hide();
    control = g_uiManager.find(2);
    if (control)
        control->show();
}

// 0x41A3D5
void UIH_41A3D5()
{
    UIControl* control = g_uiManager.find(0x1a);
    if (control && !(control->m_flags & 1))
    {
        if (!g_63813d)
            g_63813d = true;
    }
}

// 0x468A5B
void UIH_468A5B(int a)
{
    g_63e44c = a;
    f468968();
    if (!g_63e44c)
    {
        UIControl* control = g_uiManager.find(0x29);
        if (control)
            control->show();
    }
}

// 0x59274C
void UIH_59274C()
{
    g_638f0b = 0;
    UIControl* screen = UIH_4017E5();
    if (screen)
    {
        screen->hide();
        f4b2972();
    }
    UIControl* control = g_uiManager.find(2);
    if (control)
        control->hide();
}

// 0x616350: steps the value g_641b08 up by g_641b3c, clamped at g_6433d0
void UIH_616350()
{
    UIControl* control = g_uiManager.find(0x2cf8);
    if (control)
        control->enable();
    g_641b08 += g_641b3c;
    if (g_641b08 >= g_6433d0)
    {
        g_641b08 = g_6433d0;
        control = g_uiManager.find(0x2cf7);
        if (control)
            control->disable();
    }
    f4cb384(g_641b08);
}

// 0x6163B2: steps the value g_641b08 down by g_641b3c, clamped at g_6433c8
void UIH_6163B2()
{
    UIControl* control = g_uiManager.find(0x2cf7);
    if (control)
        control->enable();
    g_641b08 -= g_641b3c;
    if (g_641b08 <= g_6433c8)
    {
        g_641b08 = g_6433c8;
        control = g_uiManager.find(0x2cf8);
        if (control)
            control->disable();
    }
    f4cb384(g_641b08);
}

// 0x52FF4D
void UIH_52FF4D()
{
    UIControl* control = g_uiManager.find(0x1036);
    if (control)
        f52feef(control);
    control = g_uiManager.find(0x369a);
    if (control)
        f530a0e(control);
    control = g_uiManager.find(0x368f);
    if (control)
        f530aff(control);
    control = g_uiManager.find(0x368d);
    if (control)
        f530bf2(control);
}

// 0x41A2FB: timer handler (tick 0 = run now)
void UIH_41A2FB(unsigned int tick)
{
    UIControl* control = g_uiManager.find(0x10);
    if (control && !(control->m_flags & 1))
    {
        if (g_639470 || !tick || tick >= g_643688)
        {
            g_639470 = false;
            g_643688 = tick + 10000;
            f45390c();
        }
    }
}

// 0x401644: timer handler
void UIH_401644(unsigned int tick)
{
    UIControl* control = g_uiManager.find(0xe);
    if (control && !(control->m_flags & 1))
    {
        if (g_639145 || tick >= g_643670)
        {
            g_639145 = false;
            g_643670 = tick + 10000;
            f53002b();
            f52fa39();
            UIH_52FF4D();
            f4f004a();
            f4f0979();
            UIH_52F686();
        }
    }
}

// 0x41A384: timer handler
void UIH_41A384(unsigned int tick)
{
    UIControl* control = g_uiManager.find(0x1e);
    if (control && !(control->m_flags & 1))
    {
        if (g_639144 || !tick || tick >= g_63ba40)
        {
            g_639144 = false;
            g_63ba40 = tick + 10000;
            f5aeb82(0);
            f467c6f();
            f467e76(1);
            f467fc8(1);
            f5b108b();
        }
    }
}

// 0x4E6FC2
void UIH_4E6FC2()
{
    f443b60();
    UIH_443AF8(0);
    f4e6bbd();
}

// 0x4EFDF6
void UIH_4EFDF6()
{
    f5b14a4(0x323);
    f4f004a();
}

// 0x47ECC0: clears the text of controls 0x1392 and 0x1394
void UIH_47ECC0()
{
    UIControl* control = g_uiManager.find(0x1392);
    if (control)
        control->setText("", 0);
    control = g_uiManager.find(0x1394);
    if (control)
        control->setText("", 0);
}

// 0x47ED53: clears the text of controls 0x1391 and 0x1393
void UIH_47ED53()
{
    UIControl* control = g_uiManager.find(0x1391);
    if (control)
        control->setText("", 0);
    control = g_uiManager.find(0x1393);
    if (control)
        control->setText("", 0);
}

// 0x4E3F64
void UIH_4E3F64()
{
    UIControl* control = g_uiManager.find(0xbc8);
    if (control)
        control->setText("", 0);
    control = g_uiManager.find(0xbf2);
    if (control)
        control->setText("", 0);
}

// 0x4E3FD9
void UIH_4E3FD9()
{
    UIControl* control = g_uiManager.find(0xbc6);
    if (control)
        control->setText("", 0);
    control = g_uiManager.find(0xbf1);
    if (control)
        control->setText("", 0);
}

// 0x4E664A
void UIH_4E664A()
{
    UIControl* control = g_uiManager.find(0xe1b);
    if (control)
        control->setText("", 0);
    control = g_uiManager.find(0xe1d);
    if (control)
        control->setText("", 0);
}

// 0x6168C3
void UIH_6168C3()
{
    UIControl* control = g_uiManager.find(0x1391);
    if (control)
        control->vslot50(0x7fc, 0);
    control = g_uiManager.find(0x1393);
    if (control)
        control->setText("Zoo Cash", 0);
}

// 0x592FE3
void UIH_592FE3(bool on)
{
    g_638856 = on;
    UIControl* control = g_uiManager.find(0xc27);
    if (!control)
        return;
    if (on)
        control->enable();
    else
        control->disable();
}

// 0x618862: steps g_63e46c backwards through 0..3
void UIH_618862()
{
    if (--g_63e46c < 0)
        g_63e46c = 3;
    f4e673b();
    f4e6bbd();
}

// 0x618883: steps g_63e46c forwards through 0..3
void UIH_618883()
{
    if (++g_63e46c > 3)
        g_63e46c = 0;
    f4e673b();
    f4e6bbd();
}

// 0x617338: on key 0x2E, runs f48d052 and gives the control with id 0x104c the keyboard focus
void UIH_617338(int key)
{
    if (key == 0x2e)
    {
        f48d052();
        UIControl* control = g_uiManager.find(0x104c);
        if (control)
            g_uiManager.f44316b(control);
    }
}

// 0x61841D: on key 0x2E, runs f48d052 and gives the control with id 0x106d the keyboard focus
void UIH_61841D(int key)
{
    if (key == 0x2e)
    {
        f48d052();
        UIControl* control = g_uiManager.find(0x106d);
        if (control)
            g_uiManager.f44316b(control);
    }
}

// 0x618451: on key 0x2E, runs f48d052 and gives the control with id 0xedd the keyboard focus
void UIH_618451(int key)
{
    if (key == 0x2e)
    {
        f48d052();
        UIControl* control = g_uiManager.find(0xedd);
        if (control)
            g_uiManager.f44316b(control);
    }
}

// 0x589B34: gives the control with the given id the keyboard focus
void UIH_589B34(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        g_uiManager.f44316b(control);
}

// 0x58990A: shows the control linked from the control with the given id
void UIH_58990A(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control && control->m_unk74)
        control->m_unk74->show();
}

// 0x4C6F95: clears the text of 18 labels (ids 0x2B84 - 0x2B94, 0x2BA5)
void UIH_4C6F95()
{
    UIControl* control;

    control = g_uiManager.find(0x2b88);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b89);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b8a);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b8b);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b84);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b85);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b86);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b87);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b8c);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b8d);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b8e);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b8f);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b90);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b91);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b92);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b93);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2ba5);
    if (control)
        control->setText("", 0);

    control = g_uiManager.find(0x2b94);
    if (control)
        control->setText("", 0);
}

// 0x4C7486: resets the selection state, then clears the labels
void UIH_4C7486()
{
    g_63bbd0 = true;
    g_63e44c = 0;
    g_63e450 = 0;
    UIH_4C6F95();
}

// 0x4E0F12: shows the eight controls of the panel
void UIH_4E0F12()
{
    UIControl* control;

    control = g_uiManager.find(0xcbf);
    if (control)
        control->show();

    control = g_uiManager.find(0xc87);
    if (control)
        control->show();

    control = g_uiManager.find(0xcd3);
    if (control)
        control->show();

    control = g_uiManager.find(0xcd4);
    if (control)
        control->show();

    control = g_uiManager.find(0xcd1);
    if (control)
        control->show();

    control = g_uiManager.find(0xcd0);
    if (control)
        control->show();

    control = g_uiManager.find(0xce0);
    if (control)
        control->show();

    control = g_uiManager.find(0xce3);
    if (control)
        control->show();
}

// 0x615794: raises g_64e808 and disables the ten controls of the panel
void UIH_615794()
{
    g_64e808 = true;
    UIControl* control;

    control = g_uiManager.find(0x2b69);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b6a);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b6d);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b6e);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b73);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b67);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b6b);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b62);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b61);
    if (control)
        control->disable();

    control = g_uiManager.find(0x2b60);
    if (control)
        control->disable();
}

// 0x516C04: clears the counters, then refreshes the screen
void UIH_516C04()
{
    g_639158 = 0.0f;
    g_63e45c = 0.0f;
    g_63e454 = 0.0f;
    g_63e458 = 0.0f;
    g_63e468 = 0.0f;
    g_63e464 = 0.0f;
    UIH_516AD7();
}

// 0x484A32: toggles panel 0x26; a hide remembers the given id, a show of -1 restores it
void UIH_484A32(int id)
{
    UIControl* panel = g_uiManager.find(0x26);
    if (!panel)
        return;
    if (panel->m_flags & 1)
    {
        if (id != -1)
            g_64e660 = id;
        panel->hide();
    }
    else
    {
        if (id == -1)
        {
            UIControl* text = g_uiManager.find(0x6d65);
            if (text)
                text->setText("", 0);
            id = g_64e660;
        }
        f48482b(id);
    }
}

// 0x41A430: timer tick, advances g_654b14 when the interval has run out
void UIH_41A430(unsigned int t)
{
    if (!g_638f70)
    {
        g_638f70 = g_63e4a4 + t;
        return;
    }
    UIControl* control = g_uiManager.find(0x28);
    if (control && g_638f74)
    {
        if (t == 0 || t >= g_638f70)
        {
            g_638f70 = g_63e4a4 + t;
            f6162c0(++g_654b14);
        }
    }
}

// 0x617303: shows control 0x0E when the selected entity is of type g_638680
void UIH_617303()
{
    ZTEntity* entity = f410f84();
    if (entity && entity->m_type->isKindOf(&g_638680))
    {
        UIControl* control = g_uiManager.find(0xe);
        if (control)
            control->show();
    }
}

// 0x615CCE: refreshes the selected entity of type g_6387a0, then runs f616006 / f615fd7 on control 0x132D's flag
void UIH_615CCE()
{
    ZTEntity* entity = f410f84();
    if (entity && entity->m_type->isKindOf(&g_6387a0))
        f615d28(entity);
    UIControl* control = g_uiManager.find(0x132d);
    if (control)
    {
        if (control->flagBit(3))
            f616006(1);
        else
            f615fd7(1);
    }
}

// 0x41A78A: timer tick, every 10 seconds updates the selected entity of type g_638700
void UIH_41A78A(unsigned int t)
{
    UIControl* control = g_uiManager.find(9);
    if (control && !(control->m_flags & 1))
    {
        if (g_6390df || !t || t >= g_63b9dc)
        {
            g_63b9dc = t + 10000;
            ZTEntity* entity = f410f84();
            if (entity && entity->m_type->isKindOf(&g_638700))
                f46a144(entity);
            g_6390df = false;
        }
    }
}

// 0x41A413: timer tick, every second updates the selected entity
void UIH_41A413(unsigned int t)
{
    UIControl* control = g_uiManager.find(0x2e);
    if (control && !(control->m_flags & 1))
    {
        if (g_654b13 || !t || t >= g_654b0c)
        {
            g_654b13 = false;
            g_654b0c = t + 1000;
            ZTEntity* entity = f410f84();
            if (entity)
            {
                if (entity->m_type->isKindOf(&g_6387a0))
                {
                    f615d28(entity);
                    return;
                }
                f516aef();
            }
        }
    }
}

// 0x4EAE2F: sets the text of the control with the given id
void UIH_4EAE2F(unsigned short id, const _STL::string& text)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->setText(text, 0);
}

// 0x4F0264: sets the control with the given id to the string with the given text id
void UIH_4F0264(int id, int textId)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->setText(f4f00f6(textId), 0);
}

// 0x41D4DF: sets the control with the given id to the string f41d39c builds from a, b, c
void UIH_41D4DF(int id, int a, int b, int c)
{
    _STL::string text = f41d39c(a, b, c);
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->setText(text, 0);
}

// 0x41A3F3: timer tick, every second runs f48c87d on the selected entity of type g_638680
void UIH_41A3F3(unsigned int t)
{
    UIControl* control = g_uiManager.find(0x578);
    if (control && !(control->m_flags & 1))
    {
        if (g_64e6e8 || !t || t >= g_64e6e0)
        {
            g_64e6e8 = false;
            g_64e6e0 = t + 1000;
            ZTEntity* entity = f410f84();
            if (entity && entity->m_type->isKindOf(&g_638680))
                f48c87d(entity);
        }
    }
}

// 0x41A733: timer tick, every second runs f47108a on the selected entity of type g_638710
void UIH_41A733(unsigned int t)
{
    UIControl* control = g_uiManager.find(0x11);
    if (control && !(control->m_flags & 1))
    {
        if (g_63885c || !t || t >= g_643cd4)
        {
            g_63885c = false;
            g_643cd4 = t + 1000;
            ZTEntity* entity = f410f84();
            if (entity && entity->m_type->isKindOf(&g_638710))
                f47108a(entity);
        }
    }
}

// 0x4682F1: drops the selection list and its panels; control 0x41A is hidden by vslot21, g_638660 types get f4ef75b
void UIH_4682F1()
{
    g_639160.clear();
    f58b5ce(0);
    f4ef99b(0);
    UIControl* control = g_uiManager.find(0x41a);
    if (control)
        control->vslot21();
    ZTEntity* entity = f410f84();
    if (entity && entity->m_type->isKindOf(&g_638660))
        f4ef75b(0, 1);
    f4681b5();
    g_63ead4 = false;
}

// 0x41A34C: timer tick, every 5 seconds runs f488446 on the selected entity of type g_638680 while it is in the zoo
void UIH_41A34C(unsigned int t)
{
    UIControl* control = g_uiManager.find(0x15);
    if (control && !(control->m_flags & 1))
    {
        if (g_63c86e || !t || t >= g_63c870)
        {
            g_63c870 = t + 5000;
            ZTEntity* entity = f410f84();
            if (entity && g_638040->contains(entity) && entity->m_type->isKindOf(&g_638680))
                f488446(entity);
            g_63c86e = false;
        }
    }
}

// 0x41A76F: timer tick, every 5 seconds runs f4673b5 on the selected entity of type g_638690 while it is in the zoo
void UIH_41A76F(unsigned int t)
{
    UIControl* control = g_uiManager.find(6);
    if (control && !(control->m_flags & 1))
    {
        if (g_639531 || !t || t >= g_63b9c0)
        {
            g_63b9c0 = t + 5000;
            ZTEntity* entity = f410f84();
            if (entity && g_638040->contains(entity) && entity->m_type->isKindOf(&g_638690))
                f4673b5(entity);
            g_639531 = false;
        }
    }
}

// 0x41A367: timer tick, every 5 seconds runs f617d66 on the selected entity of type g_638680 while it is in the zoo
void UIH_41A367(unsigned int t)
{
    UIControl* control = g_uiManager.find(0x14);
    if (control && !(control->m_flags & 1))
    {
        if (!t || t >= g_654d18)
        {
            g_654d18 = t + 5000;
            ZTEntity* entity = f410f84();
            if (entity && g_638040->contains(entity) && entity->m_type->isKindOf(&g_638680))
                f617d66(entity);
        }
    }
}

// 0x4CA58E: selects the item g_6433c4 in list 0x2CF0 when nothing is selected, else switches to the selected one
void UIH_4CA58E()
{
    UIListBox* list = (UIListBox*)g_uiManager.find(0x2cf0);
    if (list)
    {
        int selected = list->m_unk37C;
        if (selected == -1)
            list->setSelectedIndex(g_6433c4, true);
        else if (g_6433c4 != selected)
            f50f396(selected);
    }
}

// 0x47158C: selects the row of the given entity in list 0x106d (-1 when it is not in the list)
void UIH_47158C(ZTEntity* entity)
{
    if (g_639474.empty())
        return;
    UIListBox* list = (UIListBox*)g_uiManager.find(0x106d);
    if (!list)
        return;
    int index = -1;
    if (entity)
    {
        index = 0;
        _STL::list<ZTEntity*>::iterator it = g_639474.begin();
        for (; it != g_639474.end(); ++it, ++index)
        {
            if (*it == entity)
                break;
        }
        if (it == g_639474.end())
            index = -1;
    }
    list->setSelectedIndex(index, true);
}

// 0x5B0199: selects the row of the given entity in list 0xe79 (-1 when it is not in the list)
void UIH_5B0199(ZTEntity* entity)
{
    if (g_639118.empty())
        return;
    UIListBox* list = (UIListBox*)g_uiManager.find(0xe79);
    if (!list)
        return;
    int index = -1;
    if (entity)
    {
        index = 0;
        _STL::list<ZTEntity*>::iterator it = g_639118.begin();
        for (; it != g_639118.end(); ++it, ++index)
        {
            if (*it == entity)
                break;
        }
        if (it == g_639118.end())
            index = -1;
    }
    list->setSelectedIndex(index, true);
}

// 0x4FA3A1: removes the row of the given entity (type g_638700) from list 0xe79 and raises g_639120
void UIH_4FA3A1(ZTEntity* entity)
{
    if (entity && !g_639118.empty() && entity->m_type->isKindOf(&g_638700))
    {
        int index = 0;
        for (_STL::list<ZTEntity*>::iterator it = g_639118.begin(); it != g_639118.end(); ++it, ++index)
        {
            if (*it == entity)
            {
                UIListBox* list = (UIListBox*)g_uiManager.find(0xe79);
                if (list)
                {
                    list->f4f9908(index);
                    g_639120 = true;
                }
                return;
            }
        }
    }
}

// 0x501F2B: removes the row of the given entity (type g_638710) from list 0x106d and raises g_63e334
void UIH_501F2B(ZTEntity* entity)
{
    if (entity && !g_639474.empty() && entity->m_type->isKindOf(&g_638710))
    {
        int index = 0;
        for (_STL::list<ZTEntity*>::iterator it = g_639474.begin(); it != g_639474.end(); ++it, ++index)
        {
            if (*it == entity)
            {
                UIListBox* list = (UIListBox*)g_uiManager.find(0x106d);
                if (list)
                {
                    list->f4f9908(index);
                    g_63e334 = true;
                }
                return;
            }
        }
    }
}

// 0x4EE4C9: selects the row of the given entity in list 0xedd (-1 when it is not in the list)
void UIH_4EE4C9(ZTEntity* entity)
{
    if (g_639460.empty())
        return;
    UIListBox* list = (UIListBox*)g_uiManager.find(0xedd);
    if (!list)
        return;
    int index = -1;
    if (entity)
    {
        index = 0;
        _STL::set<ZTEntity*>::iterator it = g_639460.begin();
        for (; it != g_639460.end(); ++index, ++it)
        {
            if (*it == entity)
                break;
        }
        if (it == g_639460.end())
            index = -1;
    }
    list->setSelectedIndex(index, true);
}

// ---- small handlers that look a control up by id and show / hide it (or hand it back)

// 0x4440D6: shows the control with id 0x1B
void UIH_4440D6()
{
    UIControl* control = g_uiManager.find(0x1b);
    if (control)
        control->show();
}

// 0x4440F1: shows the control with id 0x1C
void UIH_4440F1()
{
    UIControl* control = g_uiManager.find(0x1c);
    if (control)
        control->show();
}

// 0x4681B5: shows the control with id 0x29
void f4681b5()
{
    UIControl* control = g_uiManager.find(0x29);
    if (control)
        control->show();
}

// 0x47ED35: runs vslot21 on the control with id 0x44A
void UIH_47ED35()
{
    UIControl* control = g_uiManager.find(0x44a);
    if (control)
        control->vslot21();
}

// 0x4832B6: the control with id 0xC32
UIControl* UIH_4832B6()
{
    return g_uiManager.find(0xc32);
}

// 0x4881A9: shows the control with id 0x12E
void UIH_4881A9()
{
    UIControl* control = g_uiManager.find(0x12e);
    if (control)
        control->show();
}

// 0x488291: shows the control with id 0x25
void UIH_488291()
{
    UIControl* control = g_uiManager.find(0x25);
    if (control)
        control->show();
}

// 0x4A02FC: runs vslot21 on the control with id 0x3FB
void UIH_4A02FC()
{
    UIControl* control = g_uiManager.find(0x3fb);
    if (control)
        control->vslot21();
}

// 0x4A0399: hides the control with id 0x1D
void UIH_4A0399()
{
    UIControl* control = g_uiManager.find(0x1d);
    if (control)
        control->hide();
}

// 0x4A0463: shows the control with id 0x1D
void UIH_4A0463()
{
    UIControl* control = g_uiManager.find(0x1d);
    if (control)
        control->show();
}

// 0x4B2972: shows the control with id 0x26
void UIH_4B2972()
{
    UIControl* control = g_uiManager.find(0x26);
    if (control)
        control->show();
}

// 0x4B2AFD: shows the control with id 0x9
void UIH_4B2AFD()
{
    UIControl* control = g_uiManager.find(0x9);
    if (control)
        control->show();
}

// 0x4E6776: runs vslot21 on the control with id 0x3ED
void UIH_4E6776()
{
    UIControl* control = g_uiManager.find(0x3ed);
    if (control)
        control->vslot21();
}

// 0x4EE5A3: shows the control with id 0x6
void UIH_4EE5A3()
{
    UIControl* control = g_uiManager.find(0x6);
    if (control)
        control->show();
}

// 0x4EFE08: runs vslot21 on the control with id 0x100B
void UIH_4EFE08()
{
    UIControl* control = g_uiManager.find(0x100b);
    if (control)
        control->vslot21();
}

// 0x4EFFF8: runs vslot21 on the control with id 0x3F6
void UIH_4EFFF8()
{
    UIControl* control = g_uiManager.find(0x3f6);
    if (control)
        control->vslot21();
}

// 0x4F187A: the control with id 0x802
UIControl* UIH_4F187A()
{
    return g_uiManager.find(0x802);
}

// 0x4F188A: the control with id 0xE73
UIControl* UIH_4F188A()
{
    return g_uiManager.find(0xe73);
}

// 0x50F5FC: shows the control with id 0x578
void UIH_50F5FC()
{
    UIControl* control = g_uiManager.find(0x578);
    if (control)
        control->show();
}

// 0x513A12: shows the control with id 0x25
void UIH_513A12()
{
    UIControl* control = g_uiManager.find(0x25);
    if (control)
        control->show();
}

// 0x516AEF: shows the control with id 0x2E
void f516aef()
{
    UIControl* control = g_uiManager.find(0x2e);
    if (control)
        control->show();
}

// 0x5198D9: shows the control with id 0x14
void UIH_5198D9()
{
    UIControl* control = g_uiManager.find(0x14);
    if (control)
        control->show();
}

// 0x519940: shows the control with id 0x8
void UIH_519940()
{
    UIControl* control = g_uiManager.find(0x8);
    if (control)
        control->show();
}

// 0x51995B: shows the control with id 0x7
void UIH_51995B()
{
    UIControl* control = g_uiManager.find(0x7);
    if (control)
        control->show();
}

// 0x51A2C9: shows the control with id 0x3
void UIH_51A2C9()
{
    UIControl* control = g_uiManager.find(0x3);
    if (control)
        control->show();
}

// 0x51A2E4: shows the control with id 0x4
void UIH_51A2E4()
{
    UIControl* control = g_uiManager.find(0x4);
    if (control)
        control->show();
}

// 0x58B735: shows the control with id 0x15
void UIH_58B735()
{
    UIControl* control = g_uiManager.find(0x15);
    if (control)
        control->show();
}

// 0x58B750: shows the control with id 0x11
void UIH_58B750()
{
    UIControl* control = g_uiManager.find(0x11);
    if (control)
        control->show();
}

// 0x58ED04: shows the control with id 0x22
void UIH_58ED04()
{
    UIControl* control = g_uiManager.find(0x22);
    if (control)
        control->show();
}

// 0x618847: runs vslot21 on the control with id 0xDBB
void UIH_618847()
{
    UIControl* control = g_uiManager.find(0xdbb);
    if (control)
        control->vslot21();
}

// 0x618B0C: runs vslot21 on the control with id 0xD57
void UIH_618B0C()
{
    UIControl* control = g_uiManager.find(0xd57);
    if (control)
        control->vslot21();
}

// 0x618C47: runs vslot21 on the control with id 0xC2A
void UIH_618C47()
{
    UIControl* control = g_uiManager.find(0xc2a);
    if (control)
        control->vslot21();
}

// 0x46AA50: hides the control with id 0x9 while it is shown
void UIH_46AA50()
{
    UIControl* control = g_uiManager.find(0x9);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x471813: hides the control with id 0x11 while it is shown
void UIH_471813()
{
    UIControl* control = g_uiManager.find(0x11);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x474684: hides the control with id 0x29 while it is shown
void UIH_474684()
{
    UIControl* control = g_uiManager.find(0x29);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x483463: hides the control with id 0x1B while it is shown
void UIH_483463()
{
    UIControl* control = g_uiManager.find(0x1b);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x483B53: hides the control with id 0x1C while it is shown
void UIH_483B53()
{
    UIControl* control = g_uiManager.find(0x1c);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x488E4C: hides the control with id 0x15 while it is shown
void UIH_488E4C()
{
    UIControl* control = g_uiManager.find(0x15);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x48CD7A: hides the control with id 0x578 while it is shown
void UIH_48CD7A()
{
    UIControl* control = g_uiManager.find(0x578);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x4EE820: hides the control with id 0x6 while it is shown
void UIH_4EE820()
{
    UIControl* control = g_uiManager.find(0x6);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x6108D2: hides the control with id 0x1E while it is shown
void UIH_6108D2()
{
    UIControl* control = g_uiManager.find(0x1e);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x61613C: hides the control with id 0x2E while it is shown
void UIH_61613C()
{
    UIControl* control = g_uiManager.find(0x2e);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x6183FF: hides the control with id 0x14 while it is shown
void UIH_6183FF()
{
    UIControl* control = g_uiManager.find(0x14);
    if (control && (control->m_flags & 1))
        control->hide();
}

// 0x468FE4: calls vslot50 with the given value and 0 on the control with id 0x1304
void UIH_468FE4(int value)
{
    UIControl* control = g_uiManager.find(0x1304);
    if (control)
        control->vslot50(value, 0);
}

// 0x4DB2EC: calls vslot50 with the given value and 0 on the control with id 0xCBD
void UIH_4DB2EC(int value)
{
    UIControl* control = g_uiManager.find(0xcbd);
    if (control)
        control->vslot50(value, 0);
}

// 0x4E3842: calls vslot50 with the given value and 0 on the control with id 0x7E7
void UIH_4E3842(int value)
{
    UIControl* control = g_uiManager.find(0x7e7);
    if (control)
        control->vslot50(value, 0);
}

// 0x4E4890: calls vslot50 with the given value and 0 on the control with id 0xBF5
void UIH_4E4890(int value)
{
    UIControl* control = g_uiManager.find(0xbf5);
    if (control)
        control->vslot50(value, 0);
}

// 0x615FD7: shows the control with id 0x2F, then hides the control with id 0x30
void UIH_615FD7()
{
    UIControl* first = g_uiManager.find(0x2f);
    if (first)
        first->show();
    UIControl* second = g_uiManager.find(0x30);
    if (second)
        second->hide();
}

// 0x616006: hides the control with id 0x2F, then shows the control with id 0x30
void UIH_616006()
{
    UIControl* first = g_uiManager.find(0x2f);
    if (first)
        first->hide();
    UIControl* second = g_uiManager.find(0x30);
    if (second)
        second->show();
}

// 0x469009: hides the control with the given id
void UIH_469009(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->hide();
}

// 0x469027: shows the control with the given id
void UIH_469027(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->show();
}

// 0x4DDF66: clears flag 0x10 on the controls with ids 0xCBA and 0xCBB, then hides them
void UIH_4DDF66()
{
    UIControl* control = g_uiManager.find(0xcba);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
    control = g_uiManager.find(0xcbb);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
}

// 0x4E3D22: clears flag 0x10 on the controls with ids 0x7D0 and 0x7D1, then hides them
void UIH_4E3D22()
{
    UIControl* control = g_uiManager.find(0x7d0);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
    control = g_uiManager.find(0x7d1);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
}

// 0x4E58F9: clears flag 0x10 on the controls with ids 0xE5C and 0xE5D, then hides them
void UIH_4E58F9()
{
    UIControl* control = g_uiManager.find(0xe5c);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
    control = g_uiManager.find(0xe5d);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
}

// 0x4E5FF8: clears flag 0x10 on the controls with ids 0x806 and 0x807, then hides them
void UIH_4E5FF8()
{
    UIControl* control = g_uiManager.find(0x806);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
    control = g_uiManager.find(0x807);
    if (control)
    {
        control->setFlag(0x10, false);
        control->hide();
    }
}

// 0x4E28C8: sets flag 0x10 on the controls with ids 0x7FE and 0x82A, then shows them
void UIH_4E28C8()
{
    UIControl* control = g_uiManager.find(0x7fe);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
    control = g_uiManager.find(0x82a);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
}

// 0x4E3C83: sets flag 0x10 on the controls with ids 0x806 and 0x807, then shows them
void UIH_4E3C83()
{
    UIControl* control = g_uiManager.find(0x806);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
    control = g_uiManager.find(0x807);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
}

// 0x4E5F59: sets flag 0x10 on the controls with ids 0x7D0 and 0x7D1, then shows them
void UIH_4E5F59()
{
    UIControl* control = g_uiManager.find(0x7d0);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
    control = g_uiManager.find(0x7d1);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
}

// 0x4E65AB: sets flag 0x10 on the controls with ids 0xE5C and 0xE5D, then shows them
void UIH_4E65AB()
{
    UIControl* control = g_uiManager.find(0xe5c);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
    control = g_uiManager.find(0xe5d);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
}

// 0x4DCCBE: hides the controls with ids 0xCE8 and 0xCF9
void UIH_4DCCBE()
{
    UIControl* control = g_uiManager.find(0xce8);
    if (control)
        control->hide();
    control = g_uiManager.find(0xcf9);
    if (control)
        control->hide();
}

// 0x4DD7F9: shows the controls with ids 0xCE8 and 0xCF9
void UIH_4DD7F9()
{
    UIControl* control = g_uiManager.find(0xce8);
    if (control)
        control->show();
    control = g_uiManager.find(0xcf9);
    if (control)
        control->show();
}

// 0x443B60
void UIH_443B60()
{
    g_uiManager.f443dd0(0x404);
}

// 0x4715ED
void UIH_4715ED()
{
    g_uiManager.f443dd0(0xdfa);
}

// 0x4EB173
void UIH_4EB173(unsigned short id, const char* text)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->f4b1aa0(text, true);
}

// 0x4EB19A
void UIH_4EB19A(unsigned short id, void* value)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->f443bfc(value);
}

// 0x61705E
void UIH_61705E()
{
    UIControl* control = g_uiManager.find(0x1036);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(1);
}

// 0x61707B
void UIH_61707B()
{
    UIControl* control = g_uiManager.find(0x1036);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(2);
}

// 0x617098
void UIH_617098()
{
    UIControl* control = g_uiManager.find(0x369a);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(1);
}

// 0x6170B5
void UIH_6170B5()
{
    UIControl* control = g_uiManager.find(0x369a);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(2);
}

// 0x6170D2
void UIH_6170D2()
{
    UIControl* control = g_uiManager.find(0x368f);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(1);
}

// 0x6170EF
void UIH_6170EF()
{
    UIControl* control = g_uiManager.find(0x368f);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(2);
}

// 0x61710C
void UIH_61710C()
{
    UIControl* control = g_uiManager.find(0x368d);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(1);
}

// 0x617129
void UIH_617129()
{
    UIControl* control = g_uiManager.find(0x368d);
    if (control)
        static_cast<UIGraph*>(control)->f51a5ef(2);
}

// 0x443942
void UIH_443942(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
        control->show();
}

// 0x443E3E: enables the control when bit 1 of its flags is set
void UIH_443E3E(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control && control->flagBit(1))
        control->enable();
}

// 0x4DF425: disables the control when bit 1 of its flags is clear
void UIH_4DF425(int id)
{
    UIControl* control = g_uiManager.find(id);
    if (control && !control->flagBit(1))
        control->disable();
}

// 0x46954B: runs vslot21 on the control with id 0x3F2
void UIH_46954B()
{
    UIControl* control = g_uiManager.find(0x3f2);
    if (control)
        control->vslot21();
    f4ef99b(0);
}

// 0x469D97: runs vslot21 on the control with id 0x3F4
void UIH_469D97()
{
    UIControl* control = g_uiManager.find(0x3f4);
    if (control)
        control->vslot21();
    f4ef99b(0);
}

// 0x469DED: runs vslot21 on the control with id 0x41B
void UIH_469DED()
{
    UIControl* control = g_uiManager.find(0x41b);
    if (control)
        control->vslot21();
    f4ef99b(0);
}

void f58e9bb(int a);                               // 0x58E9BB
// 0x58ECE4
void UIH_58ECE4()
{
    UIControl* control = g_uiManager.find(0x20);
    if (control)
        control->show();
    f58e9bb(0);
}

// 0x48C7EF
void UIH_48C7EF()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->m_unk43C = true;
}

// 0x616231
void UIH_616231()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->m_unk43C = false;
}

// 0x416CB7
void UIH_416CB7()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4b06be(true);
}

// 0x4B071A
void UIH_4B071A()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4b06be(false);
}

// 0x47B9F3
void UIH_47B9F3()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4e1064(true);
}

// 0x47BA1A
void UIH_47BA1A()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4e1064(false);
}

// 0x489253
void UIH_489253()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4da19c(false);
}

// 0x48D052
void UIH_48D052()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f48d065(false);
}

// 0x509722
void UIH_509722()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f5096e8(true);
}

// 0x5097B8
void UIH_5097B8()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f5096e8(false);
}

// 0x618A22
void UIH_618A22()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f6097ef(false);
}

// 0x4B2355
void UIH_4B2355()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4b2322(0, 1);
}

// 0x4ED80A
void UIH_4ED80A()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4b2322(0, 1);
}

// 0x4DF56D
void UIH_4DF56D(int value)
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->m_unk370 = value;
}

void f4e0f12();                                    // 0x4E0F12
void f4e2967();                                    // 0x4E2967
void f4e28c8();                                    // 0x4E28C8
void f4e3f64();                                    // 0x4E3F64
void f4e3fd9();                                    // 0x4E3FD9
void f47ecc0();                                    // 0x47ECC0
void f47ed53();                                    // 0x47ED53
void f4e664a();                                    // 0x4E664A
void f4e66bf();                                    // 0x4E66BF
void f4e65ab();                                    // 0x4E65AB
void f4da59e(int a);                               // 0x4DA59E

// 0x4E0FE6
void UIH_4E0FE6()
{
    f4e0f12();
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4f189a(0, 0, 0, 1, 1);
}

// 0x4E2BB5
void UIH_4E2BB5()
{
    f4e2967();
    f4e28c8();
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4f189a(0, 0, 0, 1, 1);
}

// 0x4E4084
void UIH_4E4084()
{
    f4e3f64();
    f4e3fd9();
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4f189a(0, 0, 0, 1, 1);
}

// 0x6169BA
void UIH_6169BA()
{
    f47ecc0();
    f47ed53();
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4f189a(0, 0, 0, 1, 1);
}

// 0x4E6711
void UIH_4E6711()
{
    f4e664a();
    f4e66bf();
    f4e65ab();
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4f189a(0, 0, 0, 1, 1);
}

// 0x618553
void UIH_618553()
{
    g_uiManager.f443dd0(0xdfa);
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f46ab75();
}

// 0x4E5DDD
void UIH_4E5DDD()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        view->f4e5d11(1);
        f4da59e(view->f4da53a());
    }
}

// 0x4E5E04
void UIH_4E5E04()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        view->f4e5d11(-1);
        f4da59e(view->f4da53a());
    }
}

void f4e2bec(int a);                               // 0x4E2BEC
void f4e4021(int a);                               // 0x4E4021
void f47edc8(int a);                               // 0x47EDC8
void f4e1006(int a);                               // 0x4E1006

// 0x4DA138
void UIH_4DA138()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->setUnk364(g_uiManager.find(0xc88));
}

// 0x4DA168
void UIH_4DA168()
{
    UIControl* control = g_uiManager.find(0xd16);
    ZTMapView* view = UIH_4017E5();
    if (view && control)
        view->setUnk364(control);
}

// 0x4E6F87
void UIH_4E6F87(int id)
{
    if (id == 0xe12)
    {
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(g_uiManager.find(0xe12));
    }
}

// 0x4E2BA6
void UIH_4E2BA6(int id)
{
    if (id == 0x7e3)
    {
        f4e2bec(0);
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(0);
    }
}

// 0x4E4012
void UIH_4E4012(int id)
{
    if (id == 0xbcb)
    {
        f4e4021(0);
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(0);
    }
}

// 0x47EE2B
void UIH_47EE2B(int id)
{
    if (id == 0x138b)
    {
        f47edc8(0);
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(0);
    }
}

// 0x4E1079
void UIH_4E1079(int id)
{
    if (id == 0xc88)
    {
        f4e1006(0);
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(0);
    }
}

void f5b0f93();                                    // 0x5B0F93
// 0x6185D6: refreshes the selected entity when it is of type g_638710
void UIH_6185D6()
{
    g_uiManager.f443dd0(0xdfa);
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        ZTEntity* entity = view->m_unk438;
        if (entity && entity->m_type->isKindOf(&g_638710))
        {
            entity->f5017ac();
            f5b0f93();
        }
    }
}

void f4f9269();                                    // 0x4F9269

// 0x4E1091
void UIH_4E1091(int id)
{
    if (id == 0xc88)
    {
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(g_uiManager.find(0xc88));
    }
}

// 0x4E2BDA
void UIH_4E2BDA(int id)
{
    if (id == 0x7e3)
    {
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(g_uiManager.find(0x7e3));
    }
}

// 0x4E48BE
void UIH_4E48BE(int id)
{
    if (id == 0xbcb)
    {
        ZTMapView* view = UIH_4017E5();
        if (view)
            view->setUnk364(g_uiManager.find(0xbcb));
    }
}

// 0x4DD44E
void UIH_4DD44E()
{
    UIControl* control = g_uiManager.find(0xcf7);
    if (control)
        control->vslot50(0xcf4, 0);
    f4f9269();
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        view->f4dd600(false);
        view->f4dd630(false);
    }
}

// 0x48E4C4
void UIH_48E4C4()
{
    UIControl* control = g_uiManager.find(0xcf7);
    if (control)
        control->vslot50(0xcf5, 0);
    f4f9269();
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        view->f4dd600(true);
        view->f4dd630(true);
    }
}

// 0x4EF967
void UIH_4EF967(int id, bool useSecond)
{
    UIControl* control = g_uiManager.find(id);
    if (control)
    {
        if (useSecond)
        {
            control->m_unk40 = control->m_unk38;
            control->m_unk44 = control->m_unk3C;
            control->m_unk48 = true;
        }
        else
        {
            control->m_unk40 = control->m_unk30;
            control->m_unk44 = control->m_unk34;
            control->m_unk48 = false;
        }
    }
}

// 0x506FC0 (name: guess; stdcall: the original pops its two arguments)
void __stdcall UIH_506FC0(int id, bool force)
{
    UIControl* control = g_uiManager.find(id);
    if (control && !control->flagBit(1))
    {
        if (force || !control->flagBit(3))
            control->f506f04(0);
    }
}

// 0x4DD643
void UIH_4DD643()
{
    UIControl* control = g_uiManager.find(0xcf7);
    if (control)
        control->vslot50(0xcf3, 0);
    f4f9269();
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        view->f4dd600(false);
        view->f4dd630(true);
    }
}

// 0x5AC48D
void UIH_5AC48D()
{
    UIControl* control = g_uiManager.find(0xcf7);
    if (control)
        control->vslot50(0xcf6, 0);
    f4f9269();
    ZTMapView* view = UIH_4017E5();
    if (view)
    {
        view->f4dd600(true);
        view->f4dd630(false);
    }
}

// 0x46AF10
void UIH_46AF10()
{
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f46ab75();
}

// 0x474646
void UIH_474646(int id)
{
    UIControl* owner = g_uiManager.find(0x2b75);
    if (owner)
    {
        UIControl* control = g_uiManager.find(id);
        if (control && !control->flagBit(3))
        {
            owner->f4438fb(control);
            control->vslot20();
            control->vslot41();
        }
    }
}

// 0x4DDECD
void UIH_4DDECD()
{
    UIControl* control = g_uiManager.find(0xca8);
    if (control)
    {
        control->setFlag(0x10, true);
        control->show();
    }
    ZTMapView* view = UIH_4017E5();
    if (view)
        view->f4e1064(false);
}

// 0x599C18
void UIH_599C18()
{
    f4ef75b(0, 1);
}

// 0x5A55F6
void UIH_5A55F6(ZTEntity* entity, bool flag)
{
    if (entity == f410f84())
    {
        if (flag)
            f4ef75b(0, 1);
    }
}

// 0x58FF06
void UIH_58FF06()
{
    ZTEntity* entity = f410f84();
    if (entity && entity->m_type->isKindOf(&g_638680))
        f61794a(0);
}

// 0x44410C: shows the two controls 0x1B and 0x1C except the one that is passed in
void UIH_44410C(int id)
{
    if (id != 0x1b)
        UIH_4440D6();
    if (id != 0x1c)
        UIH_4440F1();
}

// 0x4E284A
void UIH_4E284A()
{
    UIControl* control = UIH_4F187A();
    if (control)
        control->vslot21();
    g_63cd60 = 0;
}

// 0x5B14A4: shows every control of the three groups except the one passed in
void f5b14a4(int except)
{
    UIH_5B135B(except);
    UIH_5B1426(except);
    UIH_4B2355();
    UIH_443AF8(except);
}

// 0x5B0F93: forces the next timer tick to run (clears the throttle of UIH_41A733)
void f5b0f93()
{
    g_63885c = true;
    UIH_41A733(0);
}

// 0x48168C
void UIH_48168C()
{
    UIControl* control = UIH_4F188A();
    if (control)
        control->vslot21();
}

// 0x4816B2
void UIH_4816B2()
{
    UIControl* control = UIH_4F188A();
    if (control)
        control->vslot20();
}

// 0x4832F9
void UIH_4832F9()
{
    UIControl* control = UIH_4832B6();
    if (control)
        control->vslot21();
}

// 0x484B9A
void f484b9a()
{
    UIH_484A32(0);
}

// 0x41739A: forces the next tick of UIH_401644
void f41739a()
{
    g_639145 = true;
    UIH_401644(0);
}

// 0x427996: forces the next tick of UIH_41A76F
void f427996()
{
    g_639531 = true;
    UIH_41A76F(0);
}

// 0x431712: forces the next tick of UIH_41A78A
void f431712()
{
    g_6390df = true;
    UIH_41A78A(0);
}

// 0x4741DE: forces the next tick of UIH_41A34C
void f4741de()
{
    g_63c86e = true;
    UIH_41A34C(0);
}

// 0x48173E
void f48173e(int textId)
{
    UIH_4F0264(0x9c43, textId);
}

// 0x47EE5D
void f47ee5d()
{
    UIH_443B60();
    UIH_443AF8(0);
    UIH_44410C(0);
}

// 0x4EF99B
void f4ef99b(bool useSecond)
{
    UIH_4EF967(0x6, useSecond);
    UIH_4EF967(0x9, useSecond);
    UIH_4EF967(0x11, useSecond);
    UIH_4EF967(0x14, useSecond);
    UIH_4EF967(0x15, useSecond);
    UIH_4EF967(0x578, useSecond);
    UIH_4EF967(0x2e, useSecond);
}
