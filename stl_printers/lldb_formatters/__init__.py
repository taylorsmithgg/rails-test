import lldb
import lldb_formatters.jetbrains_stl_formatters

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdDequeSynthProvider -x "^std::deque<.+> >(( )?&)?$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^std::deque<.+> >(( )?&)?$"')

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdDeque11SynthProvider -x "^(std::__1::)deque<.+>$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::__1::)deque<.+>$"')


lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdHashtableSynthProvider -x "^(std::tr1::)unordered_set<.+>.*"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::tr1::)unordered_set<.+>.*"')

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdHashtableSynthProvider -x "^(std::tr1::)unordered_map<.+>.*"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::tr1::)unordered_map<.+>.*"')

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdHashtable11SynthProvider -x "^(std::__1::)unordered_set<.+>.*"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::__1::)unordered_set<.+>.*"')

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdHashtable11SynthProvider -x "^(std::__1::)unordered_map<.+>.*"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::__1::)unordered_map<.+>.*"')

lldb.debugger.HandleCommand('type synthetic add -l lldb.formatters.cpp.libcxx.stdmap_SynthProvider -x "^(std::__1::)set<.+> >$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::__1::)set<.+> >$"')

lldb.debugger.HandleCommand('type synthetic add -l lldb.formatters.cpp.libcxx.stdmap_SynthProvider -x "^(std::__1::)multimap<.+> >$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::__1::)multimap<.+> >$"')

lldb.debugger.HandleCommand('type synthetic add -l lldb.formatters.cpp.libcxx.stdmap_SynthProvider -x "^(std::__1::)multiset<.+> >$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^(std::__1::)multiset<.+> >$"')

lldb.debugger.HandleCommand('type synthetic add -l lldb.formatters.cpp.gnu_libstdcpp.StdMapSynthProvider -x "^std::multimap<.+> >(( )?&)?$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^std::multimap<.+> >(( )?&)?$"')

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdSetSynthProvider -x "^std::set<.+> >(( )?&)?$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^std::set<.+> >(( )?&)?$"')

lldb.debugger.HandleCommand('type synthetic add -l lldb_formatters.jetbrains_stl_formatters.StdSetSynthProvider -x "^std::multiset<.+> >(( )?&)?$"')
lldb.debugger.HandleCommand('type summary add -F lldb_formatters.jetbrains_stl_formatters.SizeSummaryProvider -e -x "^std::multiset<.+> >(( )?&)?$"')
